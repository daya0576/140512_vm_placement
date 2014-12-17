/*****************************************************************
 Implementation of the robust taboo search of: E. Taillard
 "Robust taboo search for the quadratic assignment problem",
 Parallel Computing 17, 1991, 443-455.

 Data file format:
  n, optimum solution value
 (nxn) flow matrix,
 (nxn) distance matrix

 Copyright : E. Taillard, 1990-2004
 Standard C version with slight improvement regarding to
 1991 version: non uniform tabu duration
E. Taillard, 14.03.2006

 Compatibility: Unix and windows gcc, g++, bcc32.
 This code can be freely used for non-commercial purpose.
 Any use of this implementation or a modification of the code
 must acknowledge the work of E. Taillard

****************************************************************/
#include <stdio.h>
#include <stdlib.h>

const int infinite = 999999999;
const int FALSE = 0;
const int TRUE = 1;

typedef int*  type_vector;
typedef float** type_matrix;
  float *vcpu;
  float *vmem;
float *pcpu;
  float *pmem;
  int* vm;
int* pm;

  float pc_cpu=1.0;
  float pc_mem=1.0;

int opt;
double  somme_sol = 0.0;

/*************** L'Ecuyer random number generator ***************/
double rando()
 {
  static int x10 = 12345, x11 = 67890, x12 = 13579, /* initial value*/
             x20 = 24680, x21 = 98765, x22 = 43210; /* of seeds*/
  const int m = 2147483647; const int m2 = 2145483479;
  const int a12= 63308; const int q12=33921; const int r12=12979;
  const int a13=-183326; const int q13=11714; const int r13=2883;
  const int a21= 86098; const int q21=24919; const int r21= 7417;
  const int a23=-539608; const int q23= 3976; const int r23=2071;
  const double invm = 4.656612873077393e-10;
  int h, p12, p13, p21, p23;
  h = x10/q13; p13 = -a13*(x10-h*q13)-h*r13;
  h = x11/q12; p12 = a12*(x11-h*q12)-h*r12;
  if (p13 < 0) p13 = p13 + m; if (p12 < 0) p12 = p12 + m;
  x10 = x11; x11 = x12; x12 = p12-p13; if (x12 < 0) x12 = x12 + m;
  h = x20/q23; p23 = -a23*(x20-h*q23)-h*r23;
  h = x22/q21; p21 = a21*(x22-h*q21)-h*r21;
  if (p23 < 0) p23 = p23 + m2; if (p21 < 0) p21 = p21 + m2;
  x20 = x21; x21 = x22; x22 = p21-p23; if(x22 < 0) x22 = x22 + m2;
  if (x12 < x22) h = x12 - x22 + m; else h = x12 - x22;
  if (h == 0) return(1.0); else return(h*invm);
 }

/*********** return an integer between low and high *************/
int unif(int low, int high)
{return low + (int)((double)(high - low + 1) * rando()) ;}

void transpose(int *a, int *b) {int temp = *a; *a = *b; *b = temp;}
void transpose_vm(float *a, float *b) {float temp = *a; *a = *b; *b = temp;

}

//int min(int a, int b) {if (a < b) return(a); else return(b);}

double cube(double x) {return x*x*x;}


/*--------------------------------------------------------------*/
/*       compute the cost difference if elements i and j        */
/*         are transposed in permutation (solution) p           */
/*--------------------------------------------------------------*/
int compute_delta(int n, type_matrix a, type_matrix b,
                   type_vector p, int i, int j)
 {int d; int k;
  d = (a[i][i]-a[j][j])*(b[p[j]][p[j]]-b[p[i]][p[i]]) +
      (a[i][j]-a[j][i])*(b[p[j]][p[i]]-b[p[i]][p[j]]);
  for (k = 0; k < n; k = k + 1) if (k!=i && k!=j)
    d = d + (a[k][i]-a[k][j])*(b[p[k]][p[j]]-b[p[k]][p[i]]) +
            (a[i][k]-a[j][k])*(b[p[j]][p[k]]-b[p[i]][p[k]]);
  return(d);
 }

/*--------------------------------------------------------------*/
/*      Idem, but the value of delta[i][j] is supposed to       */
/*    be known before the transposition of elements r and s     */
/*--------------------------------------------------------------*/
int compute_delta_part(type_matrix a, type_matrix b,
                        type_vector p, type_matrix delta,
                        int i, int j, int r, int s)
  {return(delta[i][j]+(a[r][i]-a[r][j]+a[s][j]-a[s][i])*
     (b[p[s]][p[i]]-b[p[s]][p[j]]+b[p[r]][p[j]]-b[p[r]][p[i]])+
     (a[i][r]-a[j][r]+a[j][s]-a[i][s])*
     (b[p[i]][p[s]]-b[p[j]][p[s]]+b[p[j]][p[r]]-b[p[i]][p[r]]) );
  }


/*--------------------------------------------------------------*/
/*       compute the cost difference if move vm i to pm j        */
/*--------------------------------------------------------------*/
float compute_delta_vm(int n, type_matrix a, type_matrix b,
                   int* vm, int i, int j)
 {float d; int k;
  d = 0;
  for (k = 0; k < n; k = k + 1) if (k!=i)
    d = d + a[k][i]*(b[j][vm[k]]-b[vm[i]][vm[k]]);
  return(d);
 }

/*--------------------------------------------------------------*/
/*       compute the cost difference if move vm i to pm j   after s is moved to T     */
/*--------------------------------------------------------------*/
float compute_delta_part_vm(int n, type_matrix a, type_matrix b,type_matrix delta,
                   int* vm, int i, int j, int s, int t)
 {

    return(delta[i][j]+
		a[s][i]*(b[j][t]-b[vm[i]][t]-b[j][vm[s]]+b[vm[i]][vm[s]])  );

 }


void tabu_search(int n,                  /* problem size */
                 type_matrix a,          /* flows matrix */
                 type_matrix b,          /* distance matrix */
                 type_vector best_sol,   /* best solution found */
                 int *best_cost,         /* cost of best solution */
                 int tabu_duration,      /* parameter 1 (< n^2/2) */
                 int aspiration,         /* parameter 2 (> n^2/2)*/
                 int nr_iterations)      /* number of iterations */


 {type_vector p;                        /* current solution */
  type_matrix delta;                    /* store move costs */
  type_matrix tabu_list;                /* tabu status */
  int current_iteration;                /* current iteration */
  int current_cost;                     /* current sol. value */
  int i, j, k, i_retained, j_retained;  /* indices */
  int min_delta;                        /* retained move cost */
  int autorized;                        /* move not tabu? */
  int aspired;                          /* move forced? */
  int already_aspired;                  /* in case many moves forced */

  /***************** dynamic memory allocation *******************/
  p = (int*)calloc(n, sizeof(int));
  delta = (int**)calloc(n,sizeof(int*));
  for (i = 0; i < n; i = i+1) delta[i] = (int*)calloc(n, sizeof(int));
  tabu_list = (int**)calloc(n,sizeof(int*));
  for (i = 0; i < n; i = i+1) tabu_list[i] = (int*)calloc(n, sizeof(int));


  /************** current solution initialization ****************/
  for (i = 0; i < n; i = i + 1) p[i] = best_sol[i];

  /********** initialization of current solution value ***********/
  /**************** and matrix of cost of moves  *****************/
  current_cost = 0;
  for (i = 0; i < n; i = i + 1) for (j = 0; j < n; j = j + 1)
   {current_cost = current_cost + a[i][j] * b[p[i]][p[j]];
    if (i < j) {delta[i][j] = compute_delta(n, a, b, p, i, j);};
   };


  *best_cost = current_cost;

  /****************** tabu list initialization *******************/
  for (i = 0; i < n; i = i + 1) for (j = 0; j < n; j = j+1)
    tabu_list[i][j] = -(n*i + j);

  /******************** main tabu search loop ********************/
  for (current_iteration = 1; current_iteration <= nr_iterations && *best_cost > opt;
       current_iteration = current_iteration + 1)
   {/** find best move (i_retained, j_retained) **/
    i_retained = infinite;       /* in case all moves are tabu */
    j_retained = infinite;
    min_delta = infinite;
    already_aspired = FALSE;

    for (i = 0; i < n-1; i = i + 1)
      for (j = i+1; j < n; j = j+1)
       {autorized = (tabu_list[i][p[j]] < current_iteration) ||
                    (tabu_list[j][p[i]] < current_iteration);

        aspired =
         (tabu_list[i][p[j]] < current_iteration-aspiration)||
         (tabu_list[j][p[i]] < current_iteration-aspiration)||
         (current_cost + delta[i][j] < *best_cost);

        if ((aspired && !already_aspired) || /* first move aspired*/

           (aspired && already_aspired &&    /* many move aspired*/
            (delta[i][j] < min_delta)   ) || /* => take best one*/

           (!aspired && !already_aspired &&  /* no move aspired yet*/
           (delta[i][j] < min_delta) && autorized))

          {i_retained = i; j_retained = j;
           min_delta = delta[i][j];
           if (aspired) {already_aspired = TRUE;};
          };
       };

    if (i_retained == infinite) printf("All moves are tabu! \n");
    else
     {/** transpose elements in pos. i_retained and j_retained **/
      transpose(&p[i_retained], &p[j_retained]);
      /* update solution value*/
      current_cost = current_cost + delta[i_retained][j_retained];
      /* forbid reverse move for a random number of iterations*/
      tabu_list[i_retained][p[j_retained]] =
        current_iteration + (int)(cube(rando())*tabu_duration);
      tabu_list[j_retained][p[i_retained]] =
         current_iteration + (int)(cube(rando())*tabu_duration);

      /* best solution improved ?*/
      if (current_cost < *best_cost)
       {*best_cost = current_cost;
        for (k = 0; k < n; k = k+1) best_sol[k] = p[k];
        printf("Solution of value: %d found at iter. %d\n", current_cost, current_iteration);
       };

      /* update matrix of the move costs*/
      for (i = 0; i < n-1; i = i+1) for (j = i+1; j < n; j = j+1)
        if (i != i_retained && i != j_retained &&
            j != i_retained && j != j_retained)
         {delta[i][j] =
            compute_delta_part(a, b, p, delta,
                               i, j, i_retained, j_retained);}
        else
         {delta[i][j] = compute_delta(n, a, b, p, i, j);};
     };

   };
  /* free memory*/
  free(p);
  for (i=0; i < n; i = i+1) free(delta[i]); free(delta);
  for (i=0; i < n; i = i+1) free(tabu_list[i]);
  free(tabu_list);
} /* tabu*/


void tabu_search_vm(int n,                  /* problem size */
				 int m,
                 type_matrix a,          /* flows matrix */
                 type_matrix b,          /* distance matrix */
                 type_vector best_sol,   /* best solution found */
                 int *best_cost,         /* cost of best solution */
                 int tabu_duration,      /* parameter 1 (< n^2/2) */
                 int aspiration,         /* parameter 2 (> n^2/2)*/
                 int nr_iterations)      /* number of iterations */


 {type_vector p;                        /* current solution */
  type_matrix delta;                    /* store move costs */
  type_matrix tabu_list;                /* tabu status */
  int current_iteration;                /* current iteration */
  float current_cost;                     /* current sol. value */
  int i, j, k, i_retained, j_retained;  /* indices */
  int min_delta;                        /* retained move cost */
  int autorized;                        /* move not tabu? */
  int aspired;                          /* move forced? */
  int already_aspired;                  /* in case many moves forced */

  /***************** dynamic memory allocation *******************/
  p = (int*)calloc(n, sizeof(int));
  delta = (float**)calloc(n,sizeof(float*));
  for (i = 0; i < n; i = i+1) delta[i] = (float*)calloc(n, sizeof(float));
  tabu_list = (float**)calloc(n,sizeof(float*));
  for (i = 0; i < n; i = i+1) tabu_list[i] = (float*)calloc(n, sizeof(float));


  /************** current solution initialization ****************/
  for (i = 0; i < n; i = i + 1) p[i] = best_sol[i];

  /********** initialization of current solution value ***********/
  /**************** and matrix of cost of moves  *****************/
  current_cost = 0;
  for (i = 0; i < n; i = i + 1) for (j = 0; j < n; j = j + 1)
   {
	   if(i<j)
	   {
	   current_cost = current_cost + a[i][j] * b[p[i]][p[j]];
	   }

   };
  for (i = 0; i < n; i = i + 1) for (j = 0; j < m; j = j + 1)
   {
	   if(p[i]==j)
	   {
		   continue;
	   }
	   if(vcpu[i]+pcpu[j]>pc_cpu ||vmem[i]+pmem[j]>pc_mem)
	   {
		   delta[i][j] =infinite;
	   }
	   else
	   {
    delta[i][j] = compute_delta_vm(n, a, b, p, i, j);
	   }
   };

  *best_cost = current_cost;

  /****************** tabu list initialization *******************/
  for (i = 0; i < n; i = i + 1) for (j = 0; j < m; j = j+1)
    tabu_list[i][j] = -(n*i + j);

  /******************** main tabu search loop ********************/
  for (current_iteration = 1; current_iteration <= nr_iterations && *best_cost > opt;
       current_iteration = current_iteration + 1)
   {/** find best move (i_retained, j_retained) **/
    i_retained = infinite;       /* in case all moves are tabu */
    j_retained = infinite;
    min_delta = infinite;
    already_aspired = FALSE;

    for (i = 0; i < n; i = i + 1)
      for (j = 0; j < m; j = j+1)
       {

		   	   if(p[i]==j||(vcpu[i]+pcpu[j])>pc_cpu ||(vmem[i]+pmem[j])>pc_mem)
	   {
		   continue;
	   }
		   autorized = (tabu_list[i][j] < current_iteration) ;


        aspired =
         (tabu_list[i][j] < current_iteration-aspiration)||

         (current_cost + delta[i][j] < *best_cost);

        if ((aspired && !already_aspired) || /* first move aspired*/

           (aspired && already_aspired &&    /* many move aspired*/
            (delta[i][j] < min_delta)   ) || /* => take best one*/

           (!aspired && !already_aspired &&  /* no move aspired yet*/
           (delta[i][j] < min_delta) && autorized))

          {
			  i_retained = i; j_retained = j;
           min_delta = delta[i][j];
           if (aspired) {already_aspired = TRUE;};
          };
       };

    if (i_retained == infinite) printf("All moves are tabu! \n");
    else
     {/** transpose elements in pos. i_retained and j_retained **/
      //transpose(&p[i_retained], &p[j_retained]);

	  pcpu[p[i_retained]]-=vcpu[i_retained];
	  pmem[p[i_retained]]-=vmem[i_retained];
	  pcpu[j_retained]+=vcpu[i_retained];
	  pmem[j_retained]+=vmem[i_retained];
	  if(pcpu[p[i_retained]]<-0.00001)
	  {
		  printf("error:%10f\n",pcpu[p[i_retained]]);
		  printf("error:%10f\n",pcpu[p[i_retained]]);
	  }
	  p[i_retained]=j_retained;

      /* update solution value*/
      current_cost = current_cost + delta[i_retained][j_retained];
      /* forbid reverse move for a random number of iterations*/
      tabu_list[i_retained][p[j_retained]] =
        current_iteration + (int)(cube(rando())*tabu_duration);
      //tabu_list[j_retained][p[i_retained]] =
         //current_iteration + (int)(cube(rando())*tabu_duration);

      /* best solution improved ?*/
      if (current_cost < *best_cost)
       {*best_cost = current_cost;
        for (k = 0; k < n; k = k+1) best_sol[k] = p[k];
        printf("Solution of value: %f found at iter. %d |%d -> %d|cpu(%f , %f)| mem(%f , %f)\n", current_cost, current_iteration,i_retained,j_retained,vcpu[i_retained],pcpu[j_retained],vmem[i_retained],pmem[j_retained]);
        //show_pm_situation(n, p);
       };

      /* update matrix of the move costs*/
      for (i = 0; i < n-1; i = i+1) for (j = 0; j < m; j = j+1)
           {
	   if(p[i]==j)
	   {
		   continue;
	   }
	   if(vcpu[i]+pcpu[j]>pc_cpu ||vmem[i]+pmem[j]>pc_mem)
	   {
		   delta[i][j] =infinite;
	   }
	   else if (i != i_retained && i != j_retained &&
            j != i_retained && j != j_retained)
	   {
		   delta[i][j] = compute_delta_part_vm(n, a, b, delta,p, i, j,i_retained, j_retained);
		   /*if(delta[i][j] !=0)
		   {
		   printf("Delta short=%d \n",delta[i][j]);
		   delta[i][j] = compute_delta_vm(n, a, b, p, i, j);
		   printf("Delta long=%d \n",delta[i][j]);
		   }*/
	   }
	   else
	   {
			delta[i][j] = compute_delta_vm(n, a, b, p, i, j);
	   }
   };
     };

   };
  /* free memory*/
  free(p);
  for (i=0; i < n; i = i+1) free(delta[i]); free(delta);
  for (i=0; i < n; i = i+1) free(tabu_list[i]);
  free(tabu_list);
} /* tabu*/

void generate_random_solution(int n, type_vector  p)
 {
  int i, k;
  //for (i = 0; i < n;   i++) p[i] = i;
  for (i = 1; i < n-1; i++){
		 k = unif(i, n-1);

		  transpose(&p[i], &p[k]);
		  //transpose(&vm[i], &vm[k]);

		  transpose_vm(&pcpu[p[i]], &pcpu[p[k]]);
		  transpose_vm(&pmem[p[i]], &pmem[p[k]]);
  }
   for (i = 0; i < n; i++){
		  //printf("%f\t",pcpu[p[i]]-vcpu[i]);
		  printf("%f\t",pcpu[p[i]]);
   }

}


//read data
// empty vm and pm
void init_bestfit_solution(int n, type_vector  p){
  FILE* data_file;
  char file_name[100];
  int i;
  //strcpy(file_name, "F:\\git\\workspace\\140512_vm_sort_original\\1_MC_BT_result\\nodes_result.data");
  strcpy(file_name, "F:\\git\\workspace\\140512_vm_sort_original\\1_MC_BT_result\\tubo_solution.data");
  data_file = fopen(file_name,"r");
  printf("Open file %s ...\n",file_name);
  if (data_file != NULL)
  {
  for (i = 0; i < n; i = i+1)
  {
    fscanf(data_file,"%d", &p[i]);
    //printf("%d\n", p[i]);
  }
   printf("Read Nodes Result OK\n");
  fclose(data_file);
  }else{
    printf("file input error");
    exit(0);
  }

  // init pms
  for (i = 0; i < n; i = i+1)
  {
	  vm[i] = p[i];
  }
  for (i = 0; i < n; i = i+1)
  {
    pcpu[p[i]] += vcpu[i];
    pmem[p[i]] += vmem[i];
  }


 }

void show_pm_situation(int n, type_vector  p){
    printf("---------show_pm_situation------\n");
    int i;
    for (i = 0; i < n; i = i+1){
        printf("%f %f\n", pcpu[i], pmem[i]);
    }

    printf("--------------------------------\n");
}

int main()
 {
	 int n=1024;   //vm size                 /* problem size */
	 int m =1024;  //pm size
    int k =0;
  type_matrix a, b;         /* flows and distances matrices*/
  float ** c;
  float sol;
  type_vector solution;     /* solution (permutation) */
  int cost;                 /* solution cost */
  int nr_iterations=1800,        /* number of tabu search iterations */
      nr_resolutions=1, no_res; /* number of trials */

  FILE* data_file;
  char file_name[100];
  int i, j;
  char bidon[1000];



  opt=1024;


  /************** read file name and problem size ***************/




  /****************** dynamic memory allocation ******************/
  solution = (int*)calloc(n, sizeof(int));

  a = (int**)calloc(n, sizeof(int*));
  for (i = 0; i < n; i = i+1) a[i] = (int*)calloc(n, sizeof(int));
  b = (int**)calloc(n,sizeof(int*));
  for (i = 0; i < n; i = i+1) b[i] = (int*)calloc(n, sizeof(int));

    c = (float**)calloc(n,sizeof(float*));
  for (i = 0; i < n; i = i+1) c[i] = (float*)calloc(n, sizeof(float));


  vm = (int*)calloc(n,sizeof(int*));
  pm = (int*)calloc(m,sizeof(int*));

  vcpu = (float*)calloc(n,sizeof(float*));
  vmem = (float*)calloc(n,sizeof(float*));
  pcpu = (float*)calloc(n,sizeof(float*));
  pmem = (float*)calloc(n,sizeof(float*));


  /************** read flows and distances matrices **************/

    printf("Input Traffic Matrix Data file name :\n");
    // scanf("%s",file_name);
    //data_file = fopen(file_name,"r");
    strcpy(file_name,"F:\\git\\workspace\\140512_vm_sort_original\\input\\vm_flow_matrix\\5Partitions@15percent.data");
    data_file = fopen(file_name,"r");
    printf("Open file %s ...\n",file_name);
    if (data_file != NULL)
    {
    for (i = 0; i < n; i++) for (j = 0; j < n; j = j+1)
    {
    fscanf(data_file,"%f", &c[i][j]);
    a[i][j]=(int)c[i][j];
    /*if(a[i][j]>0)
    printf("%d ...\n",a[i][j]);*/
    }

    printf("Read Trafic Matrix Data OK\n");
    fclose(data_file);

    for (i = 0; i < n; i++) for (j = i; j < n; j = j+1){
        //if(c[i][j]>0)
        //printf("%d %d %f\n",i,j,c[i][j]);
    }

  }else{
        printf("file input error");
        exit(0);
    }

    printf("Input Cost Matrix Data file name :\n");
 //// scanf("%s",file_name);
  //data_file = fopen(file_name,"r");
  strcpy(file_name,"F:\\git\\workspace\\140512_vm_sort_original\\input\\pm_distance\\pm_distanc_1024.data");
  data_file = fopen(file_name,"r");
  printf("Open file %s ...\n",file_name);
  if (data_file != NULL)
  {
  for (i = 0; i < n; i = i+1) for (j = 0; j < n; j = j+1)
  {
      fscanf(data_file,"%f", &b[i][j]);
   /* if(b[i][j]<5)
	  printf("%f ...\n",b[i][j]);*/
  }
   printf("Read Cost Matrix Data OK\n");
  fclose(data_file);

  }else{
        printf("file input ");
        exit(0);
    }


  //read vm cpu and mem

printf("Input VM cpu and mem Data file name :\n");
  //scanf("%s",file_name);
  //data_file = fopen(file_name,"r");
  strcpy(file_name,"F:\\git\\workspace\\140512_vm_sort_original\\input\\vm_cost\\Node1024_cpu0.2_men0.2_stdvar1");
  data_file = fopen(file_name,"r");
  printf("Open file %s ...\n",file_name);
  if (data_file != NULL)
  {
  for (i = 0; i < n; i = i+1)
  {
    fscanf(data_file,"%f %f", &vcpu[i],&vmem[i]);

	  //printf("%d  %d\n", vcpu[i], vmem[i]);
  }
   printf("Read  VM cpu and mem Data OK\n");
  fclose(data_file);

  }else{
        printf("file input error");
        exit(0);
    }


    for (i = 0; i < m; i = i+1)
  {
	  pm[i]=0;
	  pcpu[i]=0;
	  pmem[i]=0;
  }


 //   printf("Init VM PM mapping :\n");
 // //scanf("%s",file_name);
 // //data_file = fopen(file_name,"r");
 // data_file = fopen("e:\\4","r");
 // printf("Open file %s ...\n",file_name);
 // if (data_file != NULL)
 // {

	//  int v,p;
 //   while(fscanf(data_file,"%d : %d", &v,&p)==2)
	//{
	//vm[v]=p;
	//pm[p]++;
	//  pcpu[p]+=vcpu[v];
	//  pmem[p]+=vmem[v];
	//}


	//  for (i = 0; i < n; i = i+1)
 // {
	//
	//  if(vm[i]==0)
	//  {
	//	  for (j = k; j < m; j = j+1)
	//	  {
	//		  if(pm[j]==0)
	//		  {
	//			    vm[i]=j;
	//			  	  pm[j]=1;
	//  pcpu[j]=vcpu[i];
	//  pmem[j]=vmem[i];
	//  k=j+1;
	//  //printf("%d -> %d\n",i,j);
	//  break;
	//		  }
	//	  }
	//  }
 //  /* if(b[i][j]<5)
	//  printf("%d ...\n",b[i][j]);*/
 // }

 //  printf("init mapping OK\n");
 // fclose(data_file);
 //
 // }

 // init vm-pm mapping
/*  for (i = 0; i < n; i = i+1)
  {
	  vm[i]=i;
  }
 for (i = 0; i < m; i = i+1)
  {
	  pm[i]=1;
	  pcpu[i]=vcpu[i];
	  pmem[i]=vmem[i];
  }
*/

    printf("Start tabu_search ...\n");

    init_bestfit_solution(n, solution);
    //init_vm_solution(n, solution);
    show_pm_situation(n, solution);

  for(no_res = 1; no_res <= nr_resolutions; no_res++)
   {
	   //generate_sort_solution(n, solution,a);
	  //generate_random_solution(n, solution);


	 /*for (i = 0; i < n;   i++) solution[i] = vm[i];
	      for (i = 0; i < n; i++)

	  {
		  printf("%f\t",pcpu[solution[i]]-vcpu[i]);
   }*/
	  //sol=0.0;
	  //  for (i = 0; i < n; i = i + 1) for (j = 0; j < n; j = j + 1)
   //{
	  // if(i<j)
	  // {
	  // sol = sol + c[i][j] * (float)b[solution[i]][solution[j]];
	  // }
   //
   //};

    tabu_search_vm(n,m, c, b,                     /* problem data */
               solution, &cost,              /* tabu search results */
               8*n, n*n*5,                   /* parameters */
               nr_iterations);               /* number of iterations */

    printf("\n %d Solution found by tabu search:\n", cost);
    for (i = 0; i < n; i = i+1) printf("%d ", solution[i]);
    printf("\n");
    somme_sol += cost;
   }

   printf("Average cost: %f, average dev: %f\n",
          somme_sol/nr_resolutions, 100*(somme_sol/nr_resolutions - opt)/opt);
    show_pm_situation(n, solution);

  free(solution);
  for (i = 0; i < n; i = i+1) free(b[i]);
  free(b);
  for (i = 0; i < n; i = i+1) free(a[i]);
  free(a);
  for (i = 0; i < n; i = i+1) free(c[i]);
  free(c);

//  printf("----------- vm situation ------------\n");
//  for(i=0; i<n; i++){
//     printf("%d ", vm[i]);
//  }
//  printf("-------------------------------------\n");
  /*strcpy(file_name,"F:\\git\\workspace\\140512_vm_sort_original\\1_MC_BT_result\\nodes_result(tabu_search).data");
  data_file = fopen(file_name,"r");
  printf("Open file %s ...\n",file_name);
  if (data_file != NULL)
  {
  for (i = 0; i < n; i = i+1)
  {
      fprintf(data_file,"%d ", vm[i]);
  }
   printf("Read Cost Matrix Data OK\n");
  fclose(data_file);

  }else{
        printf("file input ");
        exit(0);
  }
*/

  free(vm);
  free(pm);
  free(vcpu);
  free(vmem);
  free(pcpu);
  free(pmem);

  fflush(stdin);
  printf("Press return to end programme\n");
  getchar();
  return EXIT_SUCCESS;
 }





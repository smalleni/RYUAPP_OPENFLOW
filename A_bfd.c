#include <stdlib.h> 
#include <stdio.h>
#include <time.h>
#include <unistd.h>
/* needed to define exit() */ 
/* needed to define getpid() */ 

void delay(int milliseconds);
int r();
int cmdline();
char c[100]; 
int comp1=0, comp2=0;

int main() 
{ 

	while(1)
	{
		comp1 = r();
		delay(5000);
		comp2 = r();
		   printf("vData from file:\n%d",comp1);
		   printf("Data from file:\n%d",comp2);
		if (comp1 == comp2)
		{
			printf("\n The link is down \n");
			cmdline();
			exit(1);		        
/* each element represents a command line argument */ 
 /* leave the environment list null */ 
 

 /* if we get here, execve failed */
			
		} 
	}
return 0;
 }

void delay(int milliseconds)
{
    long pause;
    clock_t now,then;

    pause = milliseconds*(CLOCKS_PER_SEC/1000);
    now = then = clock();
    while( (now-then) < pause )
        now = clock();
}

int r()
{   
	
	int x;

	FILE *f;
	
   if ((f=fopen("out.txt","r"))==NULL)
	{
       printf("Error! opening file");
       exit(1); /* Program exits if file pointer returns NULL. */
	}
   fscanf(f,"%[^\n]",c);
   printf("\n Data from file:omp\n%s",c);
	int result = atoi(c); 	
	 fclose(f);
   return result;
}

int cmdline()
{
char *args[] = {"ifconfig", "eth1", "down", 0};
char *env[] ={0};

printf("\n About to run /sbin/ifconfig eth1 down\n");
execv("/sbin/ifconfig", args);
printf("\n Eth1 down \n");
//perror("execve");
}

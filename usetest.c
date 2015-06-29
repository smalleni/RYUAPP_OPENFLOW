#include <sys/socket.h>
#include <linux/netlink.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h> /* needed to define exit() */ 
#include <unistd.h>
#define NETLINK_USER 31

void timer();
int i,x;
int Incoming_Packet();
void sock();
int argc;
char **argv;
int msg_len;

#define MAX_PAYLOAD 1024 /* maximum payload size*/
struct sockaddr_nl src_addr, dest_addr;
struct nlmsghdr *nlh = NULL;
struct iovec iov;
int sock_fd;
struct msghdr msg;

int main()
{
    	unsigned int x_milliseconds=0;
	unsigned int totaltime=0,count_down=0,time_left=0;
	clock_t x_startTime,x_countTime;

    sock_fd = socket(PF_NETLINK, SOCK_RAW, NETLINK_USER);
    if (sock_fd < 0)
        return -1;

    memset(&src_addr, 0, sizeof(src_addr));
    src_addr.nl_family = AF_NETLINK;
    src_addr.nl_pid = getpid(); /* self pid */

    bind(sock_fd, (struct sockaddr *)&src_addr, sizeof(src_addr));

    memset(&dest_addr, 0, sizeof(dest_addr));
    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.nl_family = AF_NETLINK;
    dest_addr.nl_pid = 0; /* For Linux Kernel */
    dest_addr.nl_groups = 0; /* unicast */

    nlh = (struct nlmsghdr *)malloc(NLMSG_SPACE(MAX_PAYLOAD));
    memset(nlh, 0, NLMSG_SPACE(MAX_PAYLOAD));
    nlh->nlmsg_len = NLMSG_SPACE(MAX_PAYLOAD);
    nlh->nlmsg_pid = getpid();
    nlh->nlmsg_flags = 0;

    strcpy(NLMSG_DATA(nlh), "Hello");

    iov.iov_base = (void *)nlh;
    iov.iov_len = nlh->nlmsg_len;
    msg.msg_name = (void *)&dest_addr;
    msg.msg_namelen = sizeof(dest_addr);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;

    printf("Sending message to kernel\n");
    sendmsg(sock_fd, &msg, 0);
    printf("Waiting for message from kernel\n");

    /* Read message from kernel */
    recvmsg(sock_fd, &msg, MSG_DONTWAIT);
    printf("Received message payload: %s\n", NLMSG_DATA(nlh));
	msg_len = strlen(NLMSG_DATA(nlh));

	if(msg_len != 0)
	{
		//printf("Debug pointer \n");	
	
	time_left =10;  // Set the Countdown time in micro seconds. (Set to 1 sec now)
while (time_left > 0 ) 
	{
		//printf("Awesomeness. \n");
		sock_fd = socket(PF_NETLINK, SOCK_RAW, NETLINK_USER);
    		if (sock_fd < 0)
        	return -1;

    memset(&src_addr, 0, sizeof(src_addr));
    src_addr.nl_family = AF_NETLINK;
    src_addr.nl_pid = getpid(); // self pid

    bind(sock_fd, (struct sockaddr *)&src_addr, sizeof(src_addr));

    memset(&dest_addr, 0, sizeof(dest_addr));
    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.nl_family = AF_NETLINK;
    dest_addr.nl_pid = 0; // For Linux Kernel 
    dest_addr.nl_groups = 0; // unicast

    nlh = (struct nlmsghdr *)malloc(NLMSG_SPACE(MAX_PAYLOAD));
    memset(nlh, 0, NLMSG_SPACE(MAX_PAYLOAD));
    nlh->nlmsg_len = NLMSG_SPACE(MAX_PAYLOAD);
    nlh->nlmsg_pid = getpid();
    nlh->nlmsg_flags = 0;

    strcpy(NLMSG_DATA(nlh), "Hello");

    iov.iov_base = (void *)nlh;
    iov.iov_len = nlh->nlmsg_len;
    msg.msg_name = (void *)&dest_addr;
    msg.msg_namelen = sizeof(dest_addr);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
		
		sendmsg(sock_fd, &msg, 0); 
		time_left = time_left-1;
		//printf("TIme left is %d \n",time_left);	
//Sending message to the kernel.
		//printf("Debug Point 1");
		if (recvmsg(sock_fd, &msg, MSG_DONTWAIT) > 0)
			{
			time_left = 10;
			} 
		/* x_countTime=clock(); // update timer difference
		x_milliseconds=x_countTime-x_startTime;
		time_left=count_down-x_milliseconds; // subtract to get difference.
*/
		/*		
		if(time_left < 1000)
		{	
			char *args[] = {"eth1", "-a", "eth1", 0}; // each element represents a command line argument. 
			//char *env[] = { 0 }; // leave the environment list null. 
			printf("About to run /sbin/ls because Link is Down.\n"); 
			execv("/sbin/ifconfig", args); 
			perror("execv"); // if we get here, execve failed 
			return;
		}*/
	}
	
	}
printf(" \nLink has broken down ! ! !\n");
    close(sock_fd);
return(0);
}

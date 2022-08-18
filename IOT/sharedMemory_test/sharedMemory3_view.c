#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>
#include <unistd.h>
#include "share_memory.h"

int main()
{
	int shmid;
	int i;
	SHM_INFOS *shm_info = NULL;

	void *shared_memory = (void *)0;

	// 공유메모리 공간을 만든다.
	shmid = shmget((key_t)3836, sizeof(SHM_INFOS) * SHM_INFO_COUNT, 0666 | IPC_CREAT);

	if (shmid == -1)
	{
		perror("shmget failed : ");
		exit(0);
	}

	shared_memory = shmat(shmid, (void *)0, 0666 | IPC_CREAT);
	if (shared_memory == (void *)-1)
	{
		perror("shmat attach is failed : ");
		exit(0);
	}
	shm_info = (SHM_INFOS *)shared_memory;

	while (1)
	{
		for (i = 0; i < SHM_INFO_COUNT; i++)
		{
			// if (shm_info[i].check == 0)
			// {
				fprintf(stderr, "---------- [ %d ] shared info ---------\n", i);
				fprintf(stderr, "check: [%d]\n", shm_info[i].check);
				fprintf(stderr, "loadcell_1: [%d]\n", shm_info[i].one);
				fprintf(stderr, "loadcell_2: [%d]\n", shm_info[i].two);
			// }
		}
		sleep(1);
	}
}
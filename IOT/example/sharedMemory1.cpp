#include <stdio.h>

#include <stdlib.h>

#include <sys/ipc.h>

#include <sys/shm.h>

#include <string.h>

#include <unistd.h>

typedef struct _shm_info
{

    char str_ip[40];

    unsigned int int_ip;

    unsigned int int_id;

} SHM_INFOS;

int main()

{

    int shmid;

    int i;

    SHM_INFOS *shm_info = NULL;

    void *shared_memory = (void *)0;

    // 1.번 그림의 (1)에 해당, 공유메모리 공간을 가져온다. 없을시 생성

    // shmget 세부사용법은 인터넷 검색 바람

    // shmid = shmget((key_t)3836, sizeof(SHM_INFOS) * SHM_INFO_COUNT, 0666 | IPC_CREAT);

    if (shmid == -1)

    {

        //이미 공유 메모리가 생성되어 있을 경우,

        // shmget에서 설정한 공유메모리 크기와 이미 생성된 공유메모리의 크기가 같지 않을때 발생

        perror("shmget failed : ");

        exit(0);
    }

    // 1번 그림의 (2)에 해당, 공유 메모리를 process와 연결 시킨다.

    shared_memory = shmat(shmid, (void *)0, 0);

    if (shared_memory == (void *)-1)

    {

        perror("shmat failed : ");

        exit(0);
    }

    // 공유메모리에 데이터 쓰기

    shm_info = (SHM_INFOS *)shared_memory;

    while (1)

    {

        for (i = 0; i < SHM_INFO_COUNT; i++)
        {

            snprintf(shm_info[i].str_ip, sizeof(shm_info[i].str_ip), "1.1.1.%d", i);

            shm_info[i].int_ip = 12891010 + i;

            shm_info[i].int_id = 128 + i;
        }
    }

}
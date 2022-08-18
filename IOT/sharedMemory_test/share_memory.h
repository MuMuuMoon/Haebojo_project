#ifndef __SHARE_MEMORY_H__
#define __SHARE_MEMORY_H__

#define SHM_INFO_COUNT 1

typedef struct _shm_info{
	int check=0;
	int one=1;
	int two=2;
}SHM_INFOS;
#endif//__SHARE_MEMORY_H__
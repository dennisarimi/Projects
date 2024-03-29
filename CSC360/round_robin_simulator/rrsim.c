#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "linkedlist.h"

#define MAX_BUFFER_LEN 80

taskval_t *event_list = NULL;

void print_task(taskval_t *t, void *arg) {
    printf("task %03d: %5d %3.2f %3.2f\n",
        t->id,
        t->arrival_time,
        t->cpu_request,
        t->cpu_used
    );  
}


void increment_count(taskval_t *t, void *arg) {
    int *ip;
    ip = (int *)arg;
    (*ip)++;
}


void run_simulation(int qlen, int dlen) {
    taskval_t *ready_q = NULL;
    taskval_t *temp=NULL;
    int tick = 0;
    int exit = 0;

    while(event_list != NULL){
        
        if(tick < event_list->arrival_time){
            printf("[%05d] IDLE\n", tick);
            tick++;
        }
        else {
            //remove the task from the event list and place it on the ready queue
            temp = peek_front(event_list);
            event_list = remove_front(event_list);
            ready_q = add_end(ready_q, temp);

            while(ready_q != NULL){

                //if no dispatch length is specified then dispatching a task does not incur a cost
                if(dlen == 0){
                    printf("[%05d] DISPATCHING\n", tick);
                }
                else{
                    for(int i=0; i<dlen; i++){
                        printf("[%05d] DISPATCHING\n", tick);
                        tick++;
                        //check to see if the next task's arrival time has reached because tick has increased
                        if(event_list != NULL && tick == event_list->arrival_time){
                            temp = peek_front(event_list);
                            event_list = remove_front(event_list);
                            ready_q = add_end(ready_q, temp);
                        }
                    }
                }

                for(int i=0; i<qlen; i++){
                    printf("[%05d] id=%05d req=%.2f used=%.2f\n", tick, ready_q->id, ready_q->cpu_request, ready_q->cpu_used);
                    tick++;
                    //check to see if the next task's arrival time has reached because tick has increased
                    if(event_list != NULL && tick == event_list->arrival_time){
                        temp = peek_front(event_list);
                        event_list = remove_front(event_list);
                        ready_q = add_end(ready_q, temp);
                    }

                    ready_q->cpu_used++;
                    if(ready_q->cpu_used >= ready_q->cpu_request){
                        printf("[%05d] id=%05d EXIT w=%.2f ta=%.2f\n", tick, ready_q->id, (tick-ready_q->arrival_time-ready_q->cpu_request), (float)(tick-ready_q->arrival_time));
                        //when a task is complete set EXIT flag to True and leave the for loop
                        exit = 1;
                        i = qlen;
                    }
                    
                }

                //if the EXIT flag is True remove the task from the ready queue so to dispatch the next task without rotating the queue
                if (exit){
                    ready_q = remove_front(ready_q);
                    exit = 0;
                }
                else{
                    //rotating the ready queue
                    if(ready_q != NULL){
                        temp = peek_front(ready_q);
                        ready_q = remove_front(ready_q);
                        ready_q = add_end(ready_q, temp);
                    }
                }
            }
        }
    }
}


int main(int argc, char *argv[]) {
    char   input_line[MAX_BUFFER_LEN];
    int    i;
    int    task_num;
    int    task_arrival;
    float  task_cpu;
    int    quantum_length = 1;
    int    dispatch_length = 1;

    taskval_t *temp_task;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--quantum") == 0 && i+1 < argc) {
            quantum_length = atoi(argv[i+1]);
        }
        else if (strcmp(argv[i], "--dispatch") == 0 && i+1 < argc) {
            dispatch_length = atoi(argv[i+1]);
        }
    }

    if (quantum_length == -1 || dispatch_length == -1) {
        fprintf(stderr, 
            "usage: %s --quantum <num> --dispatch <num>\n",
            argv[0]);
        exit(1);
    }

    
    while(fgets(input_line, MAX_BUFFER_LEN, stdin)) {
        sscanf(input_line, "%d %d %f", &task_num, &task_arrival,
            &task_cpu);
        temp_task = new_task();
        temp_task->id = task_num;
        temp_task->arrival_time = task_arrival;
        temp_task->cpu_request = task_cpu;
        temp_task->cpu_used = 0.0;
        event_list = add_end(event_list, temp_task);
    }

// #ifdef DEBUG
//     int num_events;
//     apply(event_list, increment_count, &num_events);
//     printf("DEBUG: # of events read into list -- %d\n", num_events);
//     printf("DEBUG: value of quantum length -- %d\n", quantum_length);
//     printf("DEBUG: value of dispatch length -- %d\n", dispatch_length);
// #endif

    run_simulation(quantum_length, dispatch_length);

    return (0);
}

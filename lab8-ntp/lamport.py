from multiprocessing import Process, Pipe
from datetime import datetime


def local_time(counter):
    # print current state
    return ' (VECTOR_TIME={}, LOCAL_TIME={})'.format(counter, datetime.now())


def calc_recv_timestamp(recv_time_stamp, counter):
    # update on receive
    for i in range(len(counter)):
        counter[i] = max(recv_time_stamp[i], counter[i])
    return counter


def event(pid, counter):
    # update on some event
    counter[pid] += 1
    print('smth happened in {}'.format(pid) + local_time(counter))
    return counter


def send_message(pipe, pid, counter):
    # send message and counter
    counter[pid] += 1
    pipe.send(('empty shell', counter))
    print('message sent from ' + str(pid) + local_time(counter))
    return counter


def recv_message(pipe, pid, counter):
    # receive message and update counters
    print("here")
    message, timestamp = pipe.recv()
    print("received")
    counter = calc_recv_timestamp(timestamp, counter)
    counter[pid] += 1
    print('message received at ' + str(pid) + local_time(counter))
    return counter


def process_a(pipe_ab):
    # define counter
    counter_a = [0, 0, 0]
    # events
    counter_a = send_message(pipe_ab, 0, counter_a)
    counter_a = send_message(pipe_ab, 0, counter_a)
    counter_a = event(0, counter_a)
    counter_a = recv_message(pipe_ab, 0, counter_a)
    counter_a = event(0, counter_a)
    counter_a = event(0, counter_a)
    counter_a = recv_message(pipe_ab, 0, counter_a)
    # final counter
    print('counter for PROCESS A {}'.format(counter_a))


def process_b(pipe_ba, pipe_bc):
    # define counter
    counter_b = [0, 0, 0]
    # events
    counter_b = recv_message(pipe_ba, 1, counter_b)
    counter_b = recv_message(pipe_ba, 1, counter_b)
    counter_b = send_message(pipe_ba, 1, counter_b)
    counter_b = recv_message(pipe_bc, 1, counter_b)
    counter_b = event(1, counter_b)
    counter_b = send_message(pipe_ba, 1, counter_b)
    counter_b = send_message(pipe_bc, 1, counter_b)
    counter_b = send_message(pipe_bc, 1, counter_b)
    # final counter
    print('counter for PROCESS B {}'.format(counter_b))


def process_c(pipe_cb):
    # define counter
    counter_c = [0, 0, 0]
    # events
    counter_c = send_message(pipe_cb, 2, counter_c)
    counter_c = recv_message(pipe_cb, 2, counter_c)
    counter_c = event(2, counter_c)
    counter_c = recv_message(pipe_cb, 2, counter_c)
    # final counter
    print('counter for PROCESS C {}'.format(counter_c))
    


if __name__ == '__main__':
    # create pipes
    pipe_ab, pipe_ba = Pipe()
    pipe_bc, pipe_cb = Pipe()

    # pid a = 0
    # pid b = 1
    # pid c = 2

    # create processes
    a_process = Process(target=process_a, args=(pipe_ab,))
    b_process = Process(target=process_b, args=(pipe_ba, pipe_bc))
    c_process = Process(target=process_c, args=(pipe_cb,))

    # start processes
    a_process.start()
    b_process.start()
    c_process.start()

    # join and wait for completion
    a_process.join()
    b_process.join()
    c_process.join()
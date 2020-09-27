from multiprocessing import Process, Pipe
from datetime import datetime


def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter, datetime.now())


def calc_recv_timestamp(recv_time_stamp, counter):
    for i in range(len(counter)):
        counter[i] = max(recv_time_stamp[i], counter[i]) + 1
    return counter


def event(pid, counter):
    counter[pid] += 1
    print('smth happened in {}'.format(pid) + local_time(counter))
    return counter


def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('empty shell', counter))
    print('message sent from ' + str(pid) + local_time(counter))
    return counter


def recv_message(pipe, pid, counter):
    print("here")
    message, timestamp = pipe.recv()
    print("received")
    counter = calc_recv_timestamp(timestamp, counter)
    print('message received at ' + str(pid) + local_time(counter))
    return counter


if __name__ == '__main__':
    pipe_ab, pipe_ba = Pipe()
    pipe_bc, pipe_cb = Pipe()

    # pid a = 0
    # pid b = 1
    # pid c = 2

    counter_a = [0, 0, 0]
    counter_b = [0, 0, 0]
    counter_c = [0, 0, 0]

    # 0
    counter_a = send_message(pipe_ab, 0, counter_a)
    counter_c = send_message(pipe_bc, 2, counter_c)

    # 1
    counter_b = recv_message(pipe_ba, 1, counter_b)
    counter_a = send_message(pipe_ab, 0, counter_a)

    # 2
    counter_b = recv_message(pipe_ba, 1, counter_b)
    counter_a = event(0, counter_a)

    # 3
    counter_b = send_message(pipe_ab, 1, counter_b)

    # 4
    counter_a = recv_message(pipe_ba, 0, counter_a)
    counter_b = recv_message(pipe_cb, 1, counter_b)

    # 5
    counter_a = event(0, counter_a)
    counter_b = event(1, counter_b)

    # 6
    counter_a = event(0, counter_a)
    counter_b = send_message(pipe_ab, 1, counter_b)

    # 7
    counter_a = recv_message(pipe_ba, 0, counter_a)
    counter_b = send_message(pipe_bc, 1, counter_b)

    # 8
    counter_c = recv_message(pipe_cb, 2, counter_c)
    counter_b = send_message(pipe_bc, 1, counter_b)

    # 9 and 10
    counter_c = event(2, counter_c)
    counter_c = recv_message(pipe_cb, 2, counter_c)

    print('counter for PROCESS A {}'.format(counter_a))
    print('counter for PROCESS B {}'.format(counter_b))
    print('counter for PROCESS C {}'.format(counter_c))
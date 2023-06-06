import threading


condition = threading.Condition()
condition_met = False

def wait_for_condition():
	global condition_met

	with condition:
		print("Thread Waiting . . . ")
		while not condition_met:
			condition.wait()
		print('Condition is met. Proceeding . . .')

def signal_connection():
	global condition_met

	with condition:
		print('Signal condition. . .')
		condition_met = True
		condition.notify()


def broadcast_condition():
	global condition_met

	with condition:
		print('Broadcasting condition . . .')
		condition_met = True
		condition.notify_all()

thread1 = threading.Thread(target = wait_for_condition)
thread2 = threading.Thread(target = signal_connection)
thread3 = threading.Thread(target = broadcast_condition)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()


#uses the threading and synchronization mechanism to coordinate the activities of the producer and consumer threads.

import threading
import time
import random

#share buffer/queue

buffer = []
BUFFER_SIZE = 0

#locks and condition to simulate the synchronization
buffer_lock = threading.Lock()
not_full = threading.Condition(buffer_lock)
not_empty = threading.Condition(buffer_lock)

#producer thread function
def producer():
	global buffer_lock

	for _ in range(10):
		#simulates random production time
		time.sleep(random.randint(1, 3))

		with not_full:
			while len(buffer) == BUFFER_SIZE:
				print("Buffer is Full, Producer is waiting. . .")
				#wait while buffer is full
				not_full.wait()

		item = random.randint(1, 100)
		buffer.append(item)
		print("Producer produced: ", item)

		#notify the consumer that buffer is not empty
		not_empty.notify()

#consumer thread function
def consumer():
	global buffer

	for _ in range(10):
		with not_empty:
			while len(buffer) == 0:
				print("Buffer is empty, Consumer is waiting. . .")
				#wait while buffer is empty
				not_empty.wait()

				item = buffer.pop(0)
				print("Consumer Consumed: ", item)

				#notify the producer that buffer not empty
				not_full.notify()

#create and start the producer||consumer thread
producer_thread = threading.Thread(target = producer)
consumer_thread = threading.Thread(target = consumer)

producer_thread.start()
consumer_thread.start()


#wait for the threads to finish
producer_thread.join()
consumer_thread.join()
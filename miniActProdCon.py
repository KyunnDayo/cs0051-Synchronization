import threading
import time

# Shared buffer/queue
order_queue = []
buffer_size = 5

# Locks and conditions to for synchronization
buffer_lock = threading.Lock()
not_full = threading.Condition(buffer_lock)
not_empty = threading.Condition(buffer_lock)

# Producer thread function (Chef)
def chef():
    global order_queue

    for order in order_queue:
        
        print("Chef is preparing order:", order)

        with not_empty:
            order_queue.remove(order)
            not_empty.notify()  # Notify the consumer that an order is prepared

# Consumer thread function (Waiter)
def waiter():
    global order_queue

    while True:
        with not_full:
            while len(order_queue) == buffer_size:
                print("Order queue is full, Waiter is waiting...")
                not_full.wait()

            order = input("Enter order: ")
            order_queue.append(order)
            print("Waiter received order:", order)

            with not_empty:
                not_empty.notify()  # Notify the chef that a new order is available

# User input for the number of orders
num_orders = int(input("Enter the number of orders: "))

# Create and start the chef and waiter threads
chef_thread = threading.Thread(target=chef)
waiter_thread = threading.Thread(target=waiter)

chef_thread.start()
waiter_thread.start()

# Wait for the waiter thread to finish taking orders
waiter_thread.join()

# Wait for the chef to finish preparing orders
chef_thread.join()
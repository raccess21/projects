import multiprocessing

def process_batch(start, end):
    lst = []
    print(f"Batch {start} started")
    for i in range(start, end):
        # Your loop logic here
        lst.append(i)
    return lst

if __name__ == "__main":
    num_loops = 10
    num_processes = 2

    # Calculate the size of each batch
    batch_size = num_loops // num_processes

    # Create a process pool
    pool = multiprocessing.Pool(processes=num_processes)

    # Split the loop into batches and run them in parallel
    batch_results = []
    print(f"Batching")
    for i in range(num_processes):
        start = i * batch_size
        end = start + batch_size
        batch_result = pool.apply_async(process_batch, (start, end))
        batch_results += batch_result

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()

    # Combine the results from the batches
    #total_result = sum(batch_result.get() for batch_result in batch_results)

    print("Total result:", batch_results)


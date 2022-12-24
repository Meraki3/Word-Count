# Nadia Ben Slima
import string
import multiprocessing
import time

filepath = r"Cequilfautliredanssavie1.txt"
out_filepath = r"C:\Users\yahbo\PycharmProjects\pythonProject1\Cequilfautliredanssavie2.txt"


def remove_punct(line):
    for character in string.punctuation:
        line = line.replace(character, "")
    return line


def remove_numb(line):
    line = ''.join((x for x in line if not x.isdigit()))
    return line


def ordered_dict(dictionary):
    sorted_values = []
    for key in dictionary:
        sorted_values.append((dictionary[key], key))
        sorted_values = sorted(sorted_values)

    sorted_values = sorted_values[::-1]
    return sorted_values


def process_l(line, word_count, lock):
    line = remove_punct(line)
    line = remove_numb(line)
    words = line.split()

    lock.acquire()
    try:
        for word in words:
            word = word.lower()
            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1
    finally:

        lock.release()


def measure_t(num_processes):
    
    manager = multiprocessing.Manager()

   
    word_count = manager.dict()

    
    lock = manager.Lock()

 
    start_time = time.time()

    
    with multiprocessing.Pool(num_processes) as pool:
        # Open the input file in read mode
        with open(filepath, 'r', encoding="utf8") as fi:
            # Process the lines in the file in parallel using the worker processes
            pool.starmap(process_l, [(line, word_count, lock) for line in fi])

    # Record the end time
    end_time = time.time()

    # Sort the word count dictionary by frequency
    sorted_word_count = ordered_dict(word_count)

    # Write to the output file the sorted word count dictionary 
    with open(out_filepath, 'w', encoding="utf8") as fo:
        for item in sorted_word_count:
            fo.write("{:<30}{:>8}\n".format(item[1], item[0]))

    # time taken to execute the script
    return end_time - start_time


if __name__ == '__main__':
    # Measure time using 1 process 1
    _process = measure_t(1)
    print("Time taken with 1 process: {:.2f} seconds".format(_process))

    # Measure time using 2 processes 2
    _processes = measure_t(2)
    print("Time taken with 2 processes: {:.2f} seconds".format(_processes))

    # Measure time using 4 processes 4
    _processess = measure_t(4)
    print("Time taken with 4 processes: {:.2f} seconds".format(_processess))

    # Measure time using 8 processes 8
    _processesss = measure_t(8)
    print("Time taken with 8 processes: {:.2f} seconds".format(_processesss))

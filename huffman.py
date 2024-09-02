import argparse
import heapq
from collections import namedtuple, Counter

# A class to represent a node in the Huffman tree
class Node(namedtuple("Node", ["left", "right"])):
    def walk(self, code, acc):
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")

class Leaf(namedtuple("Leaf", ["char"])):
    def walk(self, code, acc):
        code[self.char] = acc or "0"

def get_file_contents(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read(), None
    except Exception as e:
        return None, e

def get_huffman_codes(contents):
    # Calculate frequency of each character
    frequency = Counter(contents)

    # Build the Huffman Tree using a priority queue
    huffman_heap = []
    for char, freq in frequency.items():
        huffman_heap.append((freq, len(huffman_heap), Leaf(char)))
    heapq.heapify(huffman_heap)

    count = len(huffman_heap)
    while len(huffman_heap) > 1:
        freq1, _count1, left = heapq.heappop(huffman_heap)
        freq2, _count2, right = heapq.heappop(huffman_heap)
        heapq.heappush(huffman_heap, (freq1 + freq2, count, Node(left, right)))
        count += 1

    # Generate Huffman codes
    huffman_code = {}
    if huffman_heap:
        [(_freq, _count, root)] = huffman_heap
        root.walk(huffman_code, "")

    return huffman_code

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate Huffman codes for characters in a file.")
    parser.add_argument("file_path", help="Path to the file to be read.", type=str)
    
    # Parse arguments
    args = parser.parse_args()

    # Use the get_file_contents function to read the file
    file_contents, error = get_file_contents(args.file_path)
    
    # Check if there was an error reading the file
    if error:
        print(f"Error reading file: {error}")
        return
    
    # Get the Huffman codes
    huffman_code = get_huffman_codes(file_contents)

    # Output Huffman codes as a dictionary in JSON format for ease of use in other programs
    import json
    print(json.dumps(huffman_code, indent=2))

if __name__ == "__main__":
    main()


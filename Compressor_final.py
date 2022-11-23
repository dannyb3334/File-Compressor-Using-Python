# Huffman Coding in python
# Authors: Daniel DeBrun, https://www.programiz.com/dsa/huffman-coding
import bitarray
import bitstring

# <--------Get string from file-------->
with open('Resources/original.txt') as f:
    lines = f.readlines()
x = 0
string = ''
try:
    while True:
        #Append each section of file to array
        string = string + lines[x]
        x = x + 1
except:
    print("Successfully retrieved data from file!")

# <--------Create tree Nodes-------->
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return '%s_%s' % (self.left, self.right)


# <--------Create tree-------->
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

# <--------Calculate the frequency of each character in the given string-------->
freq = {}
for c in string:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1
#Sort array, most frequent to least
freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
nodes = freq
# <--------Append leafs of tree to an array-------->
while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
huffmanCode = huffman_code_tree(nodes[0][0])

# <--------Print Leafs of tree-------->
print(' Char | Huffman code ')
print('----------------------')
for (char, frequency) in freq:
    print(' %-4r |%12s' % (char, huffmanCode[char]))

# <--------Replace each char for corresponding code value-------->
encoded = string
for char, code in huffmanCode.items():
    encoded = encoded.replace(char, code)
    
# <--------Convert Bit String To Byte Value-------->
value = bitstring.BitArray(bin=encoded)
my_bytes = value.tobytes()
#Save binary to file
with open('Resources/compressed.bin', 'wb') as f:
    f.write(bytes(my_bytes))
    
# <--------Decompress-------->
decoded = ''
global sequence
sequence = ''
for value in encoded:
    #Add bits to sequence 1 at a time
    sequence = sequence + value
    for char, code in huffmanCode.items():
        #If bit string matches corresponding character, add to decoded variable
        if sequence == code:
            decoded = decoded + char
            sequence = ''

print("\nFinished Decompressing!\n")
#Check that the compressed file didn't loose any information
if decoded == string:
    print("\nDecompressed Matches Original!\n")
else:
    print("\nNot Identical to Original!\n")
    print(decoded)
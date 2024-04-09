# Assignment 1 code outputs

## Task 1

Convert an image from RGB to YCbCr 4:2:0 and recover it.

Below are the metrics to compare
the copied and transformed images in the RGB color space:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.48102', '0.00000'],
 ['MSE', '0.73883', '0.00000'],
 ['NRMSE', '0.00483', '0.00000'],
 ['PSNR', '49.44534', 'inf'],
 ['SSIM', '0.99853', '1.00000']]
```

## Task 3

Quantize and encode YCbCr 4:2:0 images and recover them.

Below is the Huffman codebook from quantization level to code:

```python
{0: '10000001',
 1: '10000000',
 2: '1000001',
 3: '100001',
 4: '10001',
 5: '1001',
 6: '1100',
 7: '01',
 8: '111',
 9: '0010',
 10: '00001',
 11: '00000',
 12: '0001',
 13: '101',
 14: '1101',
 15: '0011'}
```

    Below is the Huffman coding tree in Mermaid diagram syntax:

```mermaid
graph TD
    114048 --> 46189
    114048 --> 67859
    46189 --> 21124
    46189 --> 25065:7
    21124 --> 9342
    21124 --> 11782
    9342 --> 4350
    9342 --> 4992:12
    4350 --> 2127:11
    4350 --> 2223:10
    2127:11
    2223:10
    4992:12
    11782 --> 5697:9
    11782 --> 6085:15
    5697:9
    6085:15
    25065:7
    67859 --> 29119
    67859 --> 38740
    29119 --> 13400
    29119 --> 15719:13
    13400 --> 6675
    13400 --> 6725:5
    6675 --> 2444
    6675 --> 4231:4
    2444 --> 1010
    2444 --> 1434:3
    1010 --> 437
    1010 --> 573:2
    437 --> 32:1
    437 --> 405
    32:1
    405
    573:2
    1434:3
    4231:4
    6725:5
    15719:13
    38740 --> 17626
    38740 --> 21114:8
    17626 --> 8314:6
    17626 --> 9312:14
    8314:6
    9312:14
    21114:8

```
<div style="text-align:center">
<a href="http://www.dmi.unict.it/"><img src="img/unict.png" width="15%" hspace="5" target="_blank"></a>
<a style="margin-left:2%" href="http://www.unica.it/"><img src="img/unica.png" width="16%" hspace="5" target="_blank"></a>
<a style="margin-left:2%" href="https://www.ictlab.srl/"><img src="img/ictlab.png" width="20%" target="_blank"></a>
<a href="https://iplab.dmi.unict.it/"><img src="img/iplab.png" width="9%" hspace="50" target="_blank"></a>
</div>
<br><br>

<h1  style="font-family: Arial;  font-size: 40px;"><b>CNN-based first quantization estimation of double compressed JPEG images</b></h1>

<div style="font-size:15px; color:black"><b><a href="https://www.sciencedirect.com/journal/journal-of-visual-communication-and-image-representation" target="_blank">Journal of Visual Communication and Image Representation 2022</a></b></div>
<br>

<div style="font-size:15px; color:black"><b>Sebastiano Battiato<sup>1,2</sup>, Oliver Giudice<sup>2,3</sup>, Francesco Guarnera<sup>1,2</sup>, Giovanni Puglisi<sup>4</sup></b></div>
<br>
<div style="font-size:12px; color:black"><sup><b>1</b></sup> <em>Department of Mathematics and Computer Science, University of Catania, Viale Andrea Doria 6, Catania 95125, Italy</em><br>
	<sup><b>2</b></sup> <em>iCTLab s.r.l. Spinoff of University of Catania, Italy</em><br>
	<sup><b>3</b></sup> <em>Banca d'Italia, Rome, Italy</em><br>
	<sup><b>4</b></sup> <em>Department of Mathematics and Computer Science, University of Cagliari, Via Ospedale 72, Cagliari 09124, Italy</em><br>
	<br>
	<b>battiato@dmi.unict.it, oliver.giudice@bancaditalia.it, francesco.guarnera@unict.it, puglisi@unica.it</b>
	<br><br>
</div>
<div style="text-align: center; background-color: cornsilk; border-radius: 10px;margin-left: 20%;margin-right: 20%;width: 60%">

<center>
<a href="https://www.sciencedirect.com/science/article/pii/S1047320322001559"><font size="5px" ><b>DOWNLOAD PAPER</b></font></a>
</center>
<br><br>
<div style="text-align:left !important;margin-left:20%">
	@article{battiato2022cnn,<br>
<span style="margin-left: 2%">title={CNN-based first quantization estimation of double compressed JPEG images},</span><br>
<span style="margin-left: 2%">author={Battiato, Sebastiano and Giudice, Oliver and Guarnera, Francesco and Puglisi, Giovanni},</span><br>
<span style="margin-left: 2%">journal={Journal of Visual Communication and Image Representation},</span><br>
<span style="margin-left: 2%">pages={103635}</span><br>
<span style="margin-left: 2%">year={2022}</span><br>
	}
</div>

<br><br>

# JPEG First Quantization Estimation 

This program is free software: it is distributed WITHOUT ANY WARRANTY.

If you are using this software, please cite:

Battiato, Sebastiano and Giudice, Oliver and Guarnera, Francesco and Puglisi, Giovanni:
“CNN-based first quantization estimation of double compressed JPEG images",
Journal of Visual Communication and Image Representation, 2022
    
The software estimates the first 15 quantization factors (in zig-zag order) of an aligned Double compressed JPEG image.

Given the double JPEG compressed image <b>I</b>, the software read the second quantization matrix <b>Q2</b> from <b>I</b> and for each second quantization factor <b>q2</b> select the rigth trained model to predict the first quantization factor <b>q1</b>. The method is built with an ensable of 2 network trained with different items which calculate the averages of softmax to choose the <b>q1</b> predicted.

IMPORTANT: the models were trained through items with a maximum value of 22 between the first 15 quantization factors <b>q1</b> and then the prediction will give always values between 1 and 22. To test the same method with higher values you need to re-train the models. If you want to re-train the models please contact one of the author to ask the right code for training. 

128_128.jpg: 128X128 image compressed with QF1=60 e QF2=90

4288_2848.jpg: 4288X2484 image compressed with QF1=60 e QF2=90

The JPEG files (128_128.jpg and 4288_2848.jpg) have the first 15 quantization factors (in zig-zag order) equal to [13, 9, 10, 11, 10, 8, 13, 11, 10, 11, 14, 14, 13, 15, 19]

cnn_v1.py: python file to predict the quantization factor (function get_coefficients_first_compression in the main).

jpeg: executable file for DCT values extraction from file (without IDCT); it needs the executable permissions.


We tested our codes on Python 2.7 and Python 3 under Ubuntu 16.04 and 18.04 (64 bit).

<br>

## Try the code

The libraries needed to execute the code are:
```
numpy
PIL
sys
import os
subprocess
sklearn 
keras
tensorflow
```



To try our software, execute:
```
python3 cnn_v1.py
python cnn_v1.py
```






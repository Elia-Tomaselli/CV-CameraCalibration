# Progetto di Computer Vision

[Link](https://drive.google.com/drive/folders/1tIRdiU4CT_9tqHtj1EaxWvbHOXSfvXn5?usp=sharing) della cartella Google Drive con i video.

[Link](https://hanwhavision.eu/it/prodotto/pno-a9081r/) della videocamera installata al sanba.

[Link](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) dato dal tutor delle risorse OpenCV per la calibrazione intrinseca.

[Link](https://drive.google.com/drive/u/2/folders/1P6Bs7bx_CGXWCbx_5wyAnqc8fPY2SGxO) della cartella Google Drive con i risultati dei test.

# Formula proiezione

$$
   P_{\text{image}} = K \cdot [R | t] \cdot P_{\text{world}}
$$

dove $P_{\text{image}}$ e $P_{\text{world}}$ sono dei punti in coordinate omogenee:

$$P_{\text{image}} = \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

$$P_{\text{world}} = \begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}$$

e dove K, R e t sono delle matrici che rappresentano rispettivamente i parametri intrinsici, e estrinsici di rotazione e traslazione.


$$
K = 
    \begin{bmatrix}
        f_x & \gamma & c_x \\
        0 & f_y & c_y \\
        0 & 0 & 1
    \end{bmatrix}
$$

$$
[R | t] =
    \left[ \begin{array}{ccc|c}
        r_{11} & r_{12} & r_{13} & t_x \\
        r_{21} & r_{22} & r_{32} & t_y \\
        r_{31} & r_{32} & r_{33} & t_z
    \end{array} \right]
$$

Per introdurre la correzione della barrel distortion o della tangential distortion solitamente quello che viene fatto è applicare queste formule:

Per la barrel distortion la formula è

$$
P_{\text{distorted}} =
    \begin{bmatrix}
        1 + k_1 \cdot r^2 + k_2 \cdot r^4 \dotsm & 0 \\
        0 & 1 + k_1 \cdot r^2 + k_2 \cdot r^4 \dotsm \\
    \end{bmatrix} \cdot P_{\text{image}}
$$

dove $k_1$ e $k_2$ regolano l'entità della barrel distortion, e $r$ è la distanza radiale $r^2 = x^2 + y^2$ dei punti non distorti rispetto al punto principale dell'immagine.

Aggiungendo la tangential distortion la formula per la distorsione diventa

$$
\hat{x} = x (1 + k_1 r^2 + k_2 r^4 + \dotsm) + 2p_1 x y + p_2 (r^2 + x^2)
\\
\hat{y} = y (1 + k_1 r^2 + k_2 r^4 + \dotsm) + p_1 (r^2 + y^2) + 2p_2 x y
$$
che può essere visto come
$$
\hat{x} = x + \Delta{x}_{\text{radial}} + \Delta{x}_{\text{tangential}}
\\
\hat{y} = y + \Delta{y}_{\text{radial}} + \Delta{y}_{\text{tangential}}
$$

dove $p_1$ e $p_2$ regolano l'entità della tangential distortion, e $r$ uguale a sopra.
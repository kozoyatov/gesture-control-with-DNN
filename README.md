# Gesture Control With DNN Model
<h2>Description</h2>
<p>
  This project implementing a gesture TV control.
  The algorithm can classify two hand gesture when placing the hand in the green window. The first gesture change the chanel forward,     the second gesture change the chanel backward.
  I used arduino UNO to control the TV.
  For now the gesture classification works only with white background.
</p>  

<div class="gif">
<table>
  <tr>
    <td>Algorithm Example</td>
    <td>Channel Changing</td>

  </tr>
  <tr>
    <td><img src="images/gesture-example-gif.gif" width=400></td>
    <td><img src="images/TV-control-gif.gif" width=400></td>

  </tr>
 </table>
</div>

<div class="gif">
  <h2>Model</h2>
  I used MobileNetV2 as a foundation to the model with imagenet weights.  I removed the last 1000 neuron layer and  disable training of     the rest layers.
  I added few more layers (later I will train them) and I achieved the final model:
  <pre>
    base_model = MobileNetV2(weights = 'imagenet', include_top=False)
    x=base_model.output
    x=GlobalAveragePooling2D()(x)
    x=BatchNormalization()(x)
    x = Dense(3, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=x)
  </pre>
</div>  

<div class = "data_and_train">
  <h2>
    Data And Training
  </h2>
  
  
  <table>

  <tr>
    <td width=40%>
      <img src="images/data-example.png" width=100%>
      <h6 style="text-align:center">
        An example of the data-set
      </h6>
  
  </td>
    <td>
      I took 500 photos of each class and label them. The model expect to get images with shape of 224X224X3, so I had to resize each           photo before using it. Finally I used keras method preprocess_input(). To solve the dimension problem I used numpy. The following function prapering images as needed:
      <pre>
        def prepar_image(img):
          x=cv2.resize(img,(224,224))
          x=image.img_to_array(x)
          x=np.expand_dims(x,axis=0)
          x=preprocess_input(x)
          return x
      </pre>
  The model was compiled with the following parameters: optimizer='adam',loss='categorical_crossentropy. Model accuracy was over 90%.
  </td>
  </tr>  
 </table>

</div>  

<div class = "circuit">
  <h2>
    Circuit 
  </h2>
  <img src = "images/Circuit.png">
  <h3>Required Components</h3>
  <ul>
    <li>Arduino UNO</li>
    <li>220 Ohm resistor</li>
    <li>IR LED</li>
  </ul>
</div>


<div class="libraries">
  <h2>Python Libraries Needed</h2>
  <ul>
    <li>cv2</li>
    <li>numpy</li>
    <li>keras</li>
    <li>serial</li>
  </ul>
  
  <h2>Arduino Libraries Needed</h2>
  <ul>
    <li>IRremote.h (by shiriff)</li>
  </ul>
</div>


<div class = "how_to_use">
  <h2>
    How To Use  
  </h2>

  <ul>
    <li>
      First build the circuit, then connect the arduino UNO to the computer. Open the arduino program-"arduino_main.ino" which             located in "arduino" folder and update in the program your required remote signal.<br /> <br /> 
       For more information to how connect arduino to the computer click <a href="https://www.arduino.cc/en/main/howto">here.</a><br />
       To find your required signal click <a href="https://www.youtube.com/watch?v=8E3ltjnbV0c&t=1443s">here.</a><br /><br />
      </li>
    <li>
      Run the main.py program (the arduino UNO have to be connected to the computer)
   </li>


  </ul>
   <h2>Enjoy!</h2>
</div>  
  
           

import { useState, useEffect } from 'react';

export default function Product() {
  const [content, setContent] = useState();

  useEffect(() => {
    const fileInput = document.querySelector('.FILE-INPUT');
    const selectedImage = document.querySelector('.SELECTED-IMAGE');
    const predictButton = document.querySelector('.PREDICT-BUTTON');

    let base64Image;

    fileInput.addEventListener('change', () => {
      const reader = new FileReader();
      reader.onload = () => {
        let dataURL = reader.result;
        selectedImage.setAttribute('src', dataURL);
        base64Image = dataURL.replace('data:image/jpeg;base64,', '');
      };
      reader.readAsDataURL(fileInput.files[0]);
    });

    predictButton.addEventListener('click', () => {
      let message = {
        image: base64Image,
      };

      fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(message),
      })
        .then((response) => response.json())
        .then((data) => {
          const prediction = data.prediction;
          console.log(prediction);

          let message = {
            name: prediction,
          };
          fetch('http://localhost:5000/form', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(message),
          })
            .then((response) => response.json())
            .then((data) => console.log(data))
            .catch((error) => console.log(error));
        })
        .catch((error) => console.log(error));
    });
  }, []);

  return (
    <main>
      <label htmlFor='ml-food'>Upload an image</label>
      <input type='file' id='ml-food' accept='.jpg' className='FILE-INPUT' />
      <img src='' className='SELECTED-IMAGE' />
      <button className='PREDICT-BUTTON'>Predict</button>

      <form>
        <input type='radio' name='dietary-restriction' id='vegan' />
        <label htmlFor='vegan'>Vegan</label>
        <input type='radio' name='dietary-restriction' id='vegetarian' />
        <label htmlFor='vegetarian'>Vegetarian</label>
      </form>

      <p>{content}</p>
    </main>
  );
}

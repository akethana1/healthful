import { useState, useEffect } from 'react';

export default function Product() {
  const [content, setContent] = useState();

  useEffect(() => {
    const textInput = document.querySelector('.TEXT-INPUT');
    const submitButton = document.querySelector('.SUBMIT-BUTTON');
    const fileInput = document.querySelector('.FILE-INPUT');
    const selectedImage = document.querySelector('.SELECTED-IMAGE');

    fileInput.addEventListener('change', (e) => {
      selectedImage.src = URL.createObjectURL(e.target.files[0]);
    });

    submitButton.addEventListener('click', () => {
      let message = {
        name: textInput.value.toLowerCase(),
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
    });
  }, []);

  return (
    <main>
      <label htmlFor='ml-food'>Upload an image</label>
      <input type='file' id='ml-food' accept='.jpg' className='FILE-INPUT' />
      <img src='' className='SELECTED-IMAGE' />
      <button className='PREDICT-BUTTON'>Predict</button>

      <label htmlFor='food' className='block mt-96'>
        Or choose a fruit/vegetable
      </label>
      <input type='text' id='food' className='TEXT-INPUT' />
      <button className='SUBMIT-BUTTON'>Submit</button>
      <p className='TEXT-CONTENT'>{content}</p>
    </main>
  );
}

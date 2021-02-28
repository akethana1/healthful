import { useState, useEffect } from 'react';
import NavbarPage from '../components/NavbarPage';
import Menu from '../components/Menu';
import Layout from '../components/Layout';
import { data } from 'autoprefixer';

export default function Product() {
  const [recipe, setRecipe] = useState({
    title: '',
    image: '',
    ingredients: '',
    method: '',
    prep1: '',
    prep2: '',
    prep3: '',
  });

  const handleMethod = (method) => {
    return method.slice(7);
  };

  const handleIngredients = (ingredients) => {
    return ingredients.slice(12);
  };

  const handlePrepTime = (prep1) => {
    return prep1.slice(16);
  };

  const handleCookingTime = (prep2) => {
    return prep2.slice(12);
  };

  const handleServes = (prep3) => {
    return prep3.slice(6);
  };

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
            .then((data) => {
              setRecipe(data);
              console.log(data);
            })
            .catch((error) => console.log(error));
        })
        .catch((error) => console.log(error));
    });
  }, []);

  return (
    <Layout>
      <Menu />

      <main>
        <NavbarPage />

        <div className='container-page mx-auto px-12'>
          <h1 className='mt-36 font-serif text-gray-800 text-4xl'>Product</h1>

          <section className='flex items-center'>
            <div className='mr-40'>
              <label
                htmlFor='ml-food'
                className=' mt-8 cursor-pointer rounded-md bg-gray-200 w-96 h-96 grid place-items-center hover:bg-gray-300 transition'
              >
                <svg
                  xmlns='http://www.w3.org/2000/svg'
                  width='60'
                  height='60'
                  viewBox='0 0 24 24'
                  className='fill-current text-gray-400'
                >
                  <path d='M19.5 12c-2.483 0-4.5 2.015-4.5 4.5s2.017 4.5 4.5 4.5 4.5-2.015 4.5-4.5-2.017-4.5-4.5-4.5zm2.5 5h-2v2h-1v-2h-2v-1h2v-2h1v2h2v1zm-18 0l4-5.96 2.48 1.96 2.52-4 1.853 2.964c-1.271 1.303-1.977 3.089-1.827 5.036h-9.026zm10.82 4h-14.82v-18h22v7.501c-.623-.261-1.297-.422-2-.476v-5.025h-18v14h11.502c.312.749.765 1.424 1.318 2zm-9.32-11c-.828 0-1.5-.671-1.5-1.5 0-.828.672-1.5 1.5-1.5s1.5.672 1.5 1.5c0 .829-.672 1.5-1.5 1.5z' />
                </svg>
              </label>
              <input
                type='file'
                id='ml-food'
                accept='.jpg'
                className='FILE-INPUT hidden'
              />
              <h3 className='mt-8 mb-4 text-xl font-light'>
                Dietary restrictions
              </h3>
              <form action='#'>
                <input type='radio' id='test1' name='radio-group' checked />
                <label for='test1' className='pl-2'>
                  None
                </label>
                <input
                  type='radio'
                  id='test2'
                  name='radio-group'
                  className='ml-8'
                />
                <label for='test2' className='pl-2'>
                  Vegan
                </label>
                <input
                  type='radio'
                  id='test3'
                  name='radio-group'
                  className='ml-8'
                />
                <label for='test3' className='pl-2'>
                  Vegetarian
                </label>
              </form>
              <button className='PREDICT-BUTTON mt-4 py-2 rounded-lg block bg-blue-900 text-white w-full'>
                Predict
              </button>
            </div>

            <div className='shadow-xl'>
              <img
                src=''
                alt=''
                className='SELECTED-IMAGE object-cover max-w-xl'
              />
            </div>
          </section>

          <section>
            <h2 className='text-4xl font-serif text-gray-800 mt-40'>
              {recipe.title}
            </h2>
            <img src={recipe.image} className='mt-8 max-w-xl pb-16' />
            <h3 className='text-gray-800 text-3xl font-serif'>Ingredients</h3>
            <p className='mt-6 leading-loose'>
              {handleIngredients(recipe.ingredients)}
            </p>
            <h3 className='text-gray-800 text-3xl font-serif mt-8'>
              Instructions
            </h3>
            <p className='mt-6 leading-loose'>{handleMethod(recipe.method)}</p>
            <h3 className='text-gray-800 text-3xl font-serif'>Prep Time</h3>
            <p className='mt-6'>{handlePrepTime(recipe.prep1)}</p>
            <h3 className='text-gray-800 text-3xl font-serif'>Cooking Time</h3>
            <p className='mt-6'>{handleCookingTime(recipe.prep2)}</p>
            <h3 className='text-gray-800 text-3xl font-serif'>Serving Size</h3>
            <p className='mt-6'>{handleServes(recipe.prep3)}</p>
          </section>
        </div>
      </main>
    </Layout>
  );
}

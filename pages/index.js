import Image from 'next/image';
import Layout from '../components/Layout';
import Navbar from '../components/Navbar';
import Menu from '../components/Menu';

export default function Home() {
  return (
    <Layout>
      <div className='fixed bg-gray-50 w-128 h-128 top-1/2 left-1/2 transform translate-x-1/3 -translate-y-2/3 rounded-full -z-20'></div>
      <div className='fixed bg-gray-50 w-96 h-96 top-1/2 left-1/2 transform -translate-x-3/4 -translate-y-2/3 rounded-full -z-20'></div>

      <Menu />

      <main className='h-screen'>
        <Image
          src='/food.png'
          alt='Healthful hero image'
          layout='fill'
          objectFit='cover'
          quality={100}
          className='-z-10'
        />
        <Navbar />
        <div className='absolute bottom-12 flex w-full items-end px-12'>
          <div className='flex-1'>
            <h1 className='font-serif text-white text-4xl leading-tight pr-16'>
              <span className='block'>Curated Recipes,</span>
              <span className='block'>Using Machine Learning</span>
            </h1>
            <a
              href='#showcase'
              className='SHOWCASE-LINK mt-8 inline-flex items-center gap-2'
            >
              <p className='SHOWCASE-LINK-TEXT font-bold text-gray-400 transition-colors duration-300'>
                See how
              </p>
              <div className='SHOWCASE-LINK-ICON w-14 h-7 border-2 border-gray-600 rounded-full transition duration-300 text-gray-300'>
                <svg
                  width='24'
                  height='24'
                  xmlns='http://www.w3.org/2000/svg'
                  fill-rule='evenodd'
                  clip-rule='evenodd'
                  className='SHOWCASE-LINK-ARROW-1 fill-current'
                >
                  <path d='M21.883 12l-7.527 6.235.644.765 9-7.521-9-7.479-.645.764 7.529 6.236h-21.884v1h21.883z' />
                </svg>
                <svg
                  width='24'
                  height='24'
                  xmlns='http://www.w3.org/2000/svg'
                  fill-rule='evenodd'
                  clip-rule='evenodd'
                  className='SHOWCASE-LINK-ARROW-2 fill-current'
                >
                  <path d='M21.883 12l-7.527 6.235.644.765 9-7.521-9-7.479-.645.764 7.529 6.236h-21.884v1h21.883z' />
                </svg>
              </div>
            </a>
          </div>
          <a
            href='/contributors'
            className='flex-1 font-medium text-gray-500 hover:text-gray-400 transition duration-200'
          >
            Meet the team
          </a>
        </div>
      </main>

      <section className='pt-64 container-homepage mx-auto px-6' id='showcase'>
        <h2 className='font-serif text-gray-800 text-3xl'>
          Take "boring" and "unhealthy" out of your meals
        </h2>
        <h2 className='font-serif text-gray-800 text-3xl'>
          Only the best recipes for your available ingredients
        </h2>
        <h2 className='font-serif text-gray-800 text-3xl'>
          Powered by advanced machine learning algorithms
        </h2>
        <div className='h-screen'></div>
      </section>
    </Layout>
  );
}

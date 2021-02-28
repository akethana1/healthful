import Image from 'next/image';
import Link from 'next/link';
import HamburgerMenuPage from './HamburgerMenuPage';

export default function NavbarPage() {
  return (
    <>
      <nav className='flex px-12 navbar-blur shadow-lg items-center z-0'>
        <figure className='flex-1'>
          <Link href='/'>
            <a>
              <Image
                src='/logo-dark.svg'
                alt='Healthful logo'
                width={64}
                height={64}
              />
            </a>
          </Link>
        </figure>
      </nav>
      <HamburgerMenuPage />
    </>
  );
}

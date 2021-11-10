import random
import string

from captcha.image import ImageCaptcha


def random_word(n):
    """ Generate a random string

    :arg
     n(int): Number of characters to generate

    :return
     Return the generated string
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


if __name__ == '__main__':
    image = ImageCaptcha(width=300, height=90)

    captcha_ = random_word(8)

    image.write(captcha_, 'images/out.png')
    input_word = input('Please input: ')

    if captcha_ == input_word:
        print('Success!!')
    else:
        print('Typo ...')
        print('Result:', captcha_)

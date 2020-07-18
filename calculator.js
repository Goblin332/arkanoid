const calculator = (string) => {
  // string = string.replace(/ /g, '');
  string = string.trim();
  const numbers = string.split(new RegExp(/[+-*\/ ]/));
  console.log(numbers);

  const result = 1;
  return result;
};

const isNumber = (number) => typeof +number === 'number';

const isArabic = (number) => !number.match(/^[IVXLCDM]/g);

// calculator('123 - 1235');
console.log(isNumber('1234'));

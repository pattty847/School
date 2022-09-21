SELECT id, street, value, zip FROM house WHERE zip = '19140';

SELECT id, street, value, zip, bedrooms, bathrooms FROM house WHERE zip = '19128' AND bedrooms >= 3 AND bathrooms=2.0;

SELECT id, street, zip, value, first, last, sold FROM house WHERE first='Mark' AND last='Jones' AND sold=TRUE;

SELECT street, value, bedrooms, bathrooms, zip FROM house WHERE zip='19116' OR zip='19154';

SELECT id, street, value, zip, sold FROM house WHERE zip='19139' AND sold=FALSE;
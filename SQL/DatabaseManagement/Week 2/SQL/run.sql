SELECT id, manu, modelname, provider FROM Phone WHERE provider='Verizon';

SELECT id, manu, modelname, rating, provider, price FROM Phone WHERE provider='Cellular One' AND price<200;

SELECT id, manu, modelname, provider, width, height FROM Phone WHERE height < 5;

SELECT id, manu, modelname, provider, price, opersys, memory FROM Phone WHERE opersys='Windows' AND memory>=16;

SELECT id, manu, modelname, provider, rating FROM Phone WHERE manu='Apple' AND manu='Samsung';

SELECT id, manu, modelname, provider, price, opersys, smartphone, memory, rating FROM Phone WHERE smartphone=TRUE AND memory>=32 AND rating>=4 AND price > 99;

SELECT id, manu, modelname, provider, price, smartphone FROM Phone WHERE smartphone=FALSE;
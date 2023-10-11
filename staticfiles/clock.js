var hr;
  var mins;
  var secs;
  var nd;
  var countryname='India';//Change the country name here
  function addOption(selectbox,text,value){var optn = document.createElement("OPTION");
  optn.text = text;optn.value = value;selectbox.options.add(optn);}
  function addOption_list()
  {
  var countries = new Array("India","France","Australia","German","USA","Canada","UK","Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Central African Republic","Chad","China","Colombia","Comoros","Republic of the Congo","Costa Rica","Côte d'Ivoire","Croatia","Cuba","Cyprus","Czech Republic","Djibouti","Dominica","Dominican Republic","East Timor","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kenya","Korea, North","Korea, South","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau (China)","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Moldova","Monaco","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan");
  for (var i=0; i < countries.length;++i){addOption(document.drop_list.Country_list, countries[i], countries[i]);}
  var uct=new Array("+5:30","- 12","- 11","- 11","- 10","- 10","- 9:30","- 9","- 9","- 8","- 7","- 6","- 5","- 4:30","- 4","- 3:30","- 3","- 3","- 2","- 2","- 2","- 1","-1:00","-1:00");
  var e = document.getElementById("list");var strUser = e.options[e.selectedIndex].value;}function selecteval(country){
  var countries = new Array("India","France","Australia","German","USA","Canada","UK","Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Central African Republic","Chad","China","Colombia","Comoros","Republic of the Congo","Costa Rica","Côte d'Ivoire","Croatia","Cuba","Cyprus","Czech Republic","Djibouti","Dominica","Dominican Republic","East Timor","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kenya","Korea, North","Korea, South","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau (China)","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Moldova","Monaco","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan");
  var uct=new Array("+5.5","+1","+10.9","+1","-5","-5","+0","+4.5","+1","+1","+1","+1","-4","-4","+4","+1","+4","-5","+3","+6","-4","+3","+1","-6","+1","+6","-4","+1","+2","+8","+2","+0","+2","+7","+1","-1","+1","+1","+8","-5","+3","+1","-6","+0","+1","-5","+2","+1","+3","-4","-4","+9","+2","-6","+1","+3","+2","+3","+12","+2","+1","+0","+4","+1","+0","+2","-4","-6","+0","+0","-4","-5","-6","+8","+1","+0","+5.5","+3.5","+3","+0","+2","+1","-5","+9","+3","+3","+9","+9","+3","+6","+7","+2","+2","+2","+0","+1","+1","+1","+1","+8","+1","+3","+2","+8","+5","+0","+1","+12","+0","+4","+2","+1","+1","+0","+2","+6.5","+1","+12","+5.65","-6","+1","+1","+1","+4","+5");
  var newtime="";
  var out = "";for(i=0; i < countries.length; i++){
  if(countries[i]==country){newtime=calcTime(countries[i],uct[i]);out=uct[i]+":00";
  document.getElementById("coun_date").innerHTML=newtime;
  document.getElementById("cntryname").innerHTML="Current Date and Time of "+country;}
  }
  var id=document.getElementById("list");
  if (id == null) {}
  else{
  addOption_list();
  document.getElementById('sel').style.display = "none";
  }
  function calcTime(city, offset){
  var d = new Date();var utc = d.getTime() + (d.getTimezoneOffset() * 60000);var plus = utc + (3600000*offset);nd = new Date(plus);hr = nd.getHours();mins = nd.getMinutes();secs = nd.getSeconds();
  return nd.toLocaleString();
  }
  setInterval(function(){function re(el, deg){el.setAttribute('transform', 'rotate('+ deg +' 90 90)');}var hh =hr;var mm = mins;var ss = secs;if(hh==0 && mm==0 && ss==0) ss=0; else ss--;var d = new Date();re(second, 6*d.getSeconds()) ; re(minute, 6*nd.getMinutes());re(hourr, 30*(nd.getHours()%12) + nd.getMinutes()/2);}, 1000) ;
}
// 각 학과별 값 뽑기

var request = require("request");  
var cheerio = require("cheerio"); 

var url="http://my.knu.ac.kr/stpo/stpo/cour/listLectPln/list.action";

var temp="";
request(url,function(error,respone,body) {
	if(error) throw error;
	
	var $ = cheerio.load(body);

	var valueElements = $("select.sub");

	 valueElements.each(function() {
		$(this).children("option").each(function(){
		
		var data = $(this);
		temp ="vlaue : "+ data.attr("value");
		temp +=" "+data.text();
		console.log(temp);
	});					
  });
});
// 각 학과별 값 뽑기

var request = require("request");  
var cheerio = require("cheerio"); 

var base="http://my.knu.ac.kr";

var url="http://my.knu.ac.kr/stpo/stpo/cour/listLectPln/list.action?search_open_crse_cde=1101&sub=11&search_open_yr_trm=20171";


var temp="";

request(url,function(error,respone,body) {
	if(error) throw error;
		
	var $ = cheerio.load(body);

	var valueElements = $("table.courTable td.th4");

	 valueElements.each(function() {

		
		var data = $(this);
		temp=data.find("a").attr("href");
		
		var url2=base+temp;
		request(url2,function(error,respone,body) {
			if(error) throw error;
			var J = cheerio.load(body);
			var info=J("table.form tr")
			info.each(function(){	
				$(this).children("th").each(function(){
				var data2 = $(this);
				console.log(data2.text().trim());
			});
				$(this).children("td").each(function(){
				var data2 = $(this);
				console.log(data2.text().trim());
			});
			
		});
		});			
			
		
		
	});					

});

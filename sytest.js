//기본적인 sy 크롤링

var request = require("request");  
var cheerio = require("cheerio"); 

var url="http://my.knu.ac.kr/stpo/stpo/cour/listLectPln/list.action?search_open_crse_cde=1O02&sub=1O&search_open_yr_trm=20171";

var temp="";
var count=1;
request(url,function(error,respone,body) {
	if(error) throw error;
	
	var $ = cheerio.load(body);

	var upperElements = $("table.courTable tr");

	 upperElements.each(function() {
		for(i=1;i<=16;i++){
			if(i==3) continue;
			if(count==1)
				var postTitle = $(this).find("th.th"+i).text();
			else
   		 		var postTitle = $(this).find("td.th"+i).text();
			temp += postTitle.trim()+" ";
			
		}
		count++;
		console.log(temp);
		temp="";			   		

  });
});
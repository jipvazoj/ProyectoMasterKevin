function gallery(src, ind){     
	
		var img = '<img id="modalImage" src="' + src + '" class="img-responsive"/>';
		var index = parseInt(ind);
		
		nexInd = getNextIndex(ind);
		prevInd = getPrevIndex(ind);
		nexUrl = getPhoto(nexInd);
		prevUrl = getPhoto(prevInd);
		//alert("NI: " + nexInd + "\n PI: " + prevInd + "\n NU: " +nexUrl + "\n PU: "+ prevUrl + "\ CU:" + src);
		var html = '';
    	html += '<div class="col-lg-2 col-md-2 col-sm-1 con-xs-1"></div>';
    	html += '<div class="col-lg-8 col-md-8 col-sm-10 con-xs-10">';
      	html +=	'<img class="img-responsive" src="'+src+'" alt="Selected image from gallery"/>';
      	html += '<a class="left carousel-control"  onclick="gallery(\'' + prevUrl + '\',\'' + prevInd + '\')"  role="button" data-slide="prev"><span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span></a>';
  		html +=	'<a class="right carousel-control" onclick="gallery(\'' + nexUrl + '\',\'' + nexInd + '\')" role="button" data-slide="next"><span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span></a>';
      	html += '</div>';
      	html += '<div class="col-lg-2 col-md-2 col-sm-1 con-xs-1"></div>';
		
		$('#myModal .modal-body').html(html);
		$('#myModal').modal();

		$('#myModal').on('hidden.bs.modal', function(){
			$('#myModal .modal-body').html('');
		});
}

function getNextIndex(ind){
	//alert(ind +" " +document.getElementById("lastIndex").value);
	var res = parseInt(ind);
	lastIndex = document.getElementById("lastIndex").value;
	if(ind == parseInt(lastIndex)-1) return 0;
	else return res+1;
}

function getPhoto(ind){
	var id = "imggallery" + ind;
	var li = document.getElementById(id);
	var img = li.getElementsByTagName('img')[0];
	return img.src;
}

function getPrevIndex(ind){
	var res = parseInt(ind);
	lastIndex = document.getElementById("lastIndex").value;
	if(ind == 0) return parseInt(lastIndex)-1;
	else return res-1;
}
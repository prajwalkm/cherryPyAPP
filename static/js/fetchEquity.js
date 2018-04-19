function getEquity(){
	$.ajax({
		method:"GET",
		url:'/getindexapi',
		contentType: "application/json",
		success:function(data){
		// console.log(data)
		data=JSON.parse(data)
		// console.log(data)
		var i;
		var equityData='';
		$('#equitlist').empty()
		for (i = 0; i < data.length; i++) { 
			// console.log(data[i].SC_NAME)
			equityData="<div class='project-item animated slideInUp'>"
			+"<div class='project-item-title'>"
			+"<span class='name'>"+ data[i].SC_NAME+"</span>"
			+"<span class='description'>COMPANY</span>"
			+"</div>"
			+"<div class='project-item-title'>"
			+"<span class='name'>"+data[i].OPEN+"</span>"
		        // +"<i class='fas fa-chart-line'></i>"
		        +"<span class='description'><i class='fas fa-chart-line'></i>OPEN</span>"
		        +"</div>"
		        +"<div class='project-item-title'>"
		        +"<span class='name'>"+data[i].LOW+"</span>"
		        +"<span class='description'><i class='fas fa-chart-line'></i>LOW</span>"
		        +"</div>"
		        +"<div class='project-item-title'>"
		        +"<span class='name'>"+data[i].HIGH+"</span>"
		        +"<span class='description'><i class='fas fa-chart-line'></i>HIGH</span>"
		        +"</div>"
		        +"<div class='project-item-title'>"
		        +"<span class='name'>"+data[i].CLOSE+"</span>"
		        +"<span class='description'><i class='fas fa-chart-line'></i>CLOSE</span>"
		        +"</div>"
		        +'</div>'
		        $('#equitlist').append(equityData)
		    }
		    $('#company').empty();
		    $('#open').empty();
		    $('#HIGH').empty();
		    $('#LOW').empty();
		    $('#CLOSE').empty();

		    $('#company').append(data[0].SC_NAME)
		    $('#open').append(data[0].OPEN)
		    $('#HIGH').append(data[0].HIGH)
		    $('#LOW').append(data[0].LOW)
		    $('#CLOSE').append(data[0].CLOSE)
		},
		error:function(err_data){
			console.log(err_data)
		}

	})
	.always(function () {
		setTimeout(getEquity, 1500000);
	})
}

getEquity()
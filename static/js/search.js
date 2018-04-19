

$(document).ready(function(){
	$("input").keyup(function(){
		var name =$("input").val();
  			// alert(name)
  			$.ajax({
  				type:'POST',
  				url:'/searchAPI',
  				data: {searchString:name},
		// contentType: 'application/json',
		success:function(ndata){
			console.log(ndata)
		},
		error:function(errdata){
			console.log(errdata)
		}

	});
  			// console.log(name)

  		});

});

// $(document).ready(function() {
//         $("#generate-string").click(function(e) {
//           $.post("/generator", {"length": $("input[name='length']").val()})
//            .done(function(string) {
//             $("#the-string").show();
//             $("#the-string input").val(string);
//           });
//           e.preventDefault();
//         });
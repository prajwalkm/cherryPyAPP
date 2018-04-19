
var Companies=[]
$.ajax({
  method:"GET",
  url:'/getAutoFillData',
  contentType: "application/json",
  success:function(data){
    // console.log(data)
    data=JSON.parse(data)
    // console.log(data)
    Companies= data
    autofill()
  },
  error:function(err_data){
    console.log(err_data)
  }

})

function autofill(){
  $( function() {
    var availableTags = Companies
    // console.log(Companies)
    $( "#tags" ).autocomplete({
      source: availableTags
    });
  } );
}


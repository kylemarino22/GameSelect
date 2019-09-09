 $(document).ready(function() { 
    $("#submitButton").click(function() { 
    	var username = $('#username').val();
    	var password = $('#password').val() 

		$.ajax({
		    url: "http://localhost:5000/api/users",
		    type: "post", 
		    data: JSON.stringify({
				"username" : username,
				"password" : password,
				"bggAccount" : "Shaheenthebean" }),
		    contentType: 'application/json',
    		dataType: 'json',
		    success: function(response) {
		    		alert ("login success");
		    },
		    error: function(xhr) {
		        //Do Something to handle error
		        console.log(xhr);
		        alert ("login failed");
		    }

	    }); 
	});
}); 
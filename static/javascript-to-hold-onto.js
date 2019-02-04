<script>
		document.addEventListener("DOMContentLoaded", function() {
			addTemplates()
		});
		var foods = [];
        function servingHandler(serv, color, id) {
            foods.push([serv, color, id]);
            food =  "serv=" + serv + "&color=" + color + "&id=" + id;
            console.log(food);
        }
        function buttonHandler() {
			console.log(JSON.stringify(foods))
		}
        function addTemplates() {
			var source = document.getElementById("hbtemplate").innerHTML;
			var template = Handlebars.compile(source);
			var allt = document.getElementById("1");
			colors.forEach(function(item, index) {
				var context = {color: item[1], id: index, name: item[0], serv: item[2]};
				var html = template(context);
				allt.insertAdjacentHTML("beforeend", html);
				if (index == 6) {
					allt = document.getElementById("2");
				}
				if (index == 13) {
					allt = document.getElementById("3");
				}
			});
		}
    </script>

function getElementsByClassName(className, tagName, parentElement)
{
  tagName = tagName || "*";
  parentElement = parentElement || document;
  var elements = new Array();
  var regExp   = new RegExp('(^|\\s)' + className + '(\\s|$)');
  var element = parentElement.getElementsByTagName(tagName);
  for (var i=0, n=element.length; i<n; i++)
  {
    if(regExp.test(element[i].className))
    {
      elements.push(element[i]);
    }
  }
  return elements;
}

function dispdiv(){
	obj = document.getElementById('dispdiv')
	if(obj && obj.style){
		if("none" == obj.style.display){
			obj.style.display="inline-block"
		}else{
			obj.style.display="none"
		}
	}
}
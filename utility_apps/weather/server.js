const https=require('https');  //Used to make https GET requests to external API's
const express=require('express');
const cheerio=require('cheerio');//JQuery based module that allows us to parse documents in NodeJs Servers. it is an implementation of core jQuery designed specifically for the server.
const fs=require('fs');//File system module
const app=express();
app.use(express.urlencoded({extended:true}));
app.use(express.static('public'));
const endpt='https://api.openweathermap.org/data/2.5/weather?';
const apikey='212f1d3afe695fca70ba3edd45fcf6ca';

//Function for editing and sending the result html to client
function sendValue(data){
  const $=cheerio.load(fs.readFileSync('public/result.html'));//Can use any variable other than the $ as well
  $('img[id=icon]').attr('src',data.iconurl);
  $('h1[id=city]').html(data.city);
  if(data.measurement!='C' && data.measurement!='F'){
    $('p[id=temperature]').html('The temperature is: '+data.temperature+' K');
    $('p[id=dets]').html('Current weather:  '+data.description+' with a max of '+data.maximum+' '+data.measurement+' and min of '+data.minimum+' '+data.measurement);
  }
  else{
    $('p[id=temperature]').html('The temperature is: '+data.temperature+' °'+data.measurement);
    $('p[id=dets]').html('Current weather:  '+data.description+' with a max of '+data.maximum+'°'+data.measurement+' and min of '+data.minimum+'°'+data.measurement);
  }
  $('p[id=hum-det]').html('Humidity: '+data.humidity+' %');
  $('p[id=press-det]').html('Pressure: '+data.pressure+' hPa');
  fs.writeFile("public/result.html", $.html(), function(err) {
    if(err) {
      throw err;
    }
    console.log("The file was saved!");
  });
}
/*Tells the server to go to the public folder, if it encounters the reference to any other files in the html doc that it is sending on the Website. While processing the server will look into the public folder but while using functions such as the res.send(), we have to give the absolute path. The server wont look into the public folder in this case*/

app.get('/',function(req,res){
  res.send("<h1>Hello There!<h1>");
});

app.get('/weather',function(req,res){
  res.sendFile(__dirname+'/weather.html')
});

//Another way to get the static file from the server, using get requests. Better way is to use the expess static middleware
// app.get('/public/weather.css', function(req, res) {
//   res.sendFile(__dirname + "/weather.css");
// });

app.post('/weather',function(req,res){
  var city=req.body.loc;
  var unit=req.body.unit;
  var measure=unit;
  if(unit=='C')
    unit='metric';
  else if(unit=='F')
    unit='imperial';
  else if(unit=='K')
    unit='standard';
  else if(unit=='')
    unit='';
  else
    res.send("<h1>Invalid Unit. Use one of the mentioned units only</h1>");
  var url=endpt+'q='+city+'&units='+unit+'&appid='+apikey;

  https.get(url,function(response){
      //Takes only the response object as the parameter,
      //The response object contains our weather data in json and other info
      //like the status code, url, timestamp etc.
    status=response.statusCode;
    console.log(status);
    if(status==200){
      response.on('data',function(data){
        //data object is contained within response object, this callback function is called
        const wdata=JSON.parse(data);
        const iconUrl='http://openweathermap.org/img/wn/'+wdata.weather[0].icon+'@2x.png';
        const obj={
          temperature:wdata.main.temp,
          city:wdata.name,
          description:wdata.weather[0].description,
          maximum:wdata.main.temp_max,
          minimum:wdata.main.temp_min,
          humidity:wdata.main.humidity,
          pressure:wdata.main.pressure,
          iconurl:iconUrl,
          measurement:measure
        }
        sendValue(obj);
        setTimeout(function(){
          res.sendFile(__dirname+'/public/result.html');
          console.log('Result sent to client');
        },300);
      })
    }
    else {
      res.send("<h1>Sorry! We don't have data on the entered location.</h1>\n<h3>We shall add it soon!</h3>");
    }
  })
})

app.listen(process.env.PORT || 2000,function(){
  console.log("Server started on port 2000");
});

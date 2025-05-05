const express=require('express');
const app=express();
app.use(express.urlencoded({extended:true}));
app.use(express.static('public'));
app.set('view engine','ejs');
let items=[];

app.get('/',function(req,res){
  day=new Date();
  let options={
    day:'numeric',
    weekday:'long',
    month:'long',
    year:'numeric'
  };
  date=day.toLocaleDateString('en-US',options);
  components=date.split(', ');
  data={
    today1:components[0],
    today2:components[1]+', '+components[2],
    info:items
  }
  res.render('todo',data);
})

app.post('/',function(req,res){
  newitem=req.body.item;
  items.push(newitem)
  res.redirect('/');
})



app.listen(3000 || process.env.PORT,function(req,res){
  console.log("Application Started, listening on port 3000 locally!");
})


var val;



function allowDrop(ev)
{
    ev.preventDefault();
}
function dragStart(ev)
{
    val= ev.target.innerHTML;
}
function drop(ev)
{
    ev.target.innerHTML=ev.target.innerHTML+ "["+val+"]";
}
function Write()
{

    key = document.getElementById('key').value;
    o="";

    fin =document.getElementById('fin').innerHTML;
    no =document.getElementById('no').innerHTML;
    key= key.split("]",no);
    fin= fin.split("]",no);

    for (let t = 0; t <fin.length; t++)
    {
        for(let g=0; g<fin[t].length; g++)
        {
            if(fin[t][g] == "[")
            {
                o = o + key[t].replace("[", "");
               break;
            }
            else
            {
               o = o + fin[t][g];
            }
        }
    }
    document.getElementById('fin').innerHTML = o;



}

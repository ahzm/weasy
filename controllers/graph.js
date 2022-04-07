const spawn=require("child_process").spawn;
exports.graph=(req,res)=>{
    const pyProcess=spawn('python',["../python/apiGet.py",])
}
from src.components import object_proxy, defined_var, func
from src.core import script_stream

sample = """
function submit_form_as_json(request_type, form_id){
    let post_object = collect_form_inputs(form_id);
    console.log(post_object);
    make_json_request(request_type, post_object, function(data, status, xhr){
        let redir_loc = xhr.getResponseHeader("Redir-Location post_object ");
        console.log(redir_loc);
        if (redir_loc != null){
            window.location.href = redir_loc;
        }
    }, function(xhr, status, err){
        console.log(xhr.responseText);
    });
}
"""
old_len = len(sample)
s = script_stream.ScriptStream(sample)
# object_proxy.ObjectProxyComponent(s).run()
defined_var.DefinedVariableComponent(s).run()
func.AnonFunctionComponent(s).run()
print(s.resolve_symbols())
print(len(s.raw) / old_len)
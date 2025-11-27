$(function () {
    console.log("✅ pub_blog.js loaded and ready");

    // 检查 wangEditor 是否加载
    if (!window.wangEditor) {
        console.error("❌ wangEditor not loaded!");
        alert("编辑器加载失败，请刷新页面");
        return;
    }

    const { createEditor, createToolbar } = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        },
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    console.log("✅ Editor initialized");

    $("#submit-btn").click(function (event) {
        console.log("🔵 Submit button clicked");
        //阻止按钮的默认行为
        event.preventDefault();

        let title = $("input[name='title']").val();
        let category = $("#category-select").val();
        let content = editor.getHtml();
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

        console.log("📤 Sending AJAX request with data:", { title, category });

        $.ajax('/blog/pub', {
            method: 'POST',
            data: { title, category, content, csrfmiddlewaretoken },
            success: function (result) {
                console.log("✅ AJAX Success response:", result);
                if (result['code'] === 200) {
                    //跳转到博客详情
                    let blog_id = result['data']['blog_id'];
                    let targetUrl = "/blog/detail/" + blog_id;
                    console.log("🔄 Redirecting to:", targetUrl);
                    //获取博客id
                    window.location.href = targetUrl;
                } else {
                    console.warn("⚠️ Server returned non-200 code:", result);
                    alert(result['message']);
                }
            },
            error: function (xhr, status, error) {
                console.error("❌ AJAX Error:", { xhr, status, error });
                console.error("Response text:", xhr.responseText);
                alert("发布失败: " + error)
            }
        })

    })
})
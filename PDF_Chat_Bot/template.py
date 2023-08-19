css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQczRU48BbfEGxN1uv8Aa756HfWyBGhMABBJA&usqp=CAU" /></div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3d8QKDpPCuKQ8e1y0KuxR5dzT5mKeMtxANIVLM7s2YByc-ZDJmDOazuEV1ZsRTBCo3-s&usqp=CAU"/>        
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
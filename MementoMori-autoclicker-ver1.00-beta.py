import tkinter as tk
import pyautogui as pyauto
from pynput import keyboard
from pynput import mouse
import sys, os

root = tk.Tk()
root.title('MementoMori-オートクリッカー ver 1.00 beta')
root.geometry('420x280')
root.resizable(False, False)



def resource_path(relative):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative)


class autoclick():
    
    def __init__(self,root):
        self.root=root
        self.running=False
        self.create_menu()
        self.create()
        self.key_listener = keyboard.Listener(on_press=self.on_press)
        self.key_listener.start()
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
        self.auto_clicking = False
        pyauto.PAUSE = 0
    
    def create_menu(self):
        self.menu1=tk.Menu(self.root, tearoff=False)
        self.root.config(menu=self.menu1)
        self.file_menu = tk.Menu(self.menu1, tearoff=False)
        self.menu1.add_cascade(label="ファイル(制作中)", menu=self.file_menu)
        self.file_menu.add_command(label="設定の読み込み(R)")
        self.file_menu.add_command(label="設定の保存(s)")
        self.file_menu.add_command(label="終了", command=self.root.destroy)
        
        self.front_window= tk.BooleanVar(value=False)
        self.menu1.add_checkbutton(label="常に最前面に表示",variable=self.front_window,command=self.front)


    def create(self):
        self.bg_image = tk.PhotoImage(file=resource_path("autoclicker_background.png"))
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.frame1=tk.LabelFrame(self.root,text="座標登録設定")
        self.frame1.grid(row=0,column=0,sticky='ew',padx=10, pady=5,columnspan=2)
        
        self.f12label=tk.Label(self.frame1,text="F12キーで座標登録")
        self.f12label.grid(row=0,column=0,columnspan=3)
        
        self.click_time_label=tk.Label(self.frame1,text="クリック間隔")
        self.click_time_label.grid(row=1,column=0)
        
        self.input_time=tk.Entry(self.frame1,width=8,)
        self.input_time.grid(row=1,column=1)
        self.input_time.insert(0,"100")
        
        self.time_label=tk.Label(self.frame1,text="ミリ秒")
        self.time_label.grid(row=1,column=2)
        
        self.click_type = tk.IntVar(value=1)
        self.right_cluck_type=tk.Radiobutton(self.frame1,text="右クリック",variable=self.click_type,value=2)
        self.left_cluck_type=tk.Radiobutton(self.frame1,text="左クリック",variable=self.click_type,value=1)
        self.right_cluck_type.grid(row=2,column=1)
        self.left_cluck_type.grid(row=2,column=0)
        
        
        self.frame2=tk.LabelFrame(self.root,text="設定")
        self.frame2.grid(row=1,column=0,sticky='ew',padx=10, pady=2,columnspan=2)
        
        self.click_number=tk.Label(self.frame2,text="クリック回数")
        self.click_number.grid(row=0,column=0)
        
        self.input_click_number=tk.Entry(self.frame2,width=8)
        self.input_click_number.grid(row=0,column=1)
        self.input_click_number.insert(0,"0")
        
        self.label2=tk.Label(self.frame2,text="回")
        self.label2.grid(row=0,column=2)
        
        self.start_time=tk.Label(self.frame2,text="開始時間")
        self.start_time.grid(row=1,column=0)
        
        self.input_start_time=tk.Entry(self.frame2,width=8)
        self.input_start_time.grid(row=1,column=1)
        self.input_start_time.insert(0,"2")
        
        self.label1=tk.Label(self.frame2,text="秒後")
        self.label1.grid(row=1,column=2)
        
        
        self.frame3=tk.LabelFrame(self.root,text="情報")
        self.frame3.grid(row=2,column=0,sticky='ew',padx=10, pady=2,columnspan=2)
        
        self.now_inf=tk.Label(self.frame3,text="現在の状態:")
        self.now_inf.grid(row=0,column=0)
        
        self.now_inf2=tk.Label(self.frame3,text="停止中")
        self.now_inf2.grid(row=0,column=1)
        
        self.clickcount=tk.Label(self.frame3,text="現在のクリック回数:")
        self.clickcount.grid(row=1,column=0)
        
        self.clickcount2=tk.Label(self.frame3,text="0")
        self.clickcount2.grid(row=1,column=1)
        
        
        self.frame4=tk.LabelFrame(self.root,text="座標")
        self.frame4.grid(row=0,column=2,rowspan=3,padx=5, pady=2,sticky='ns',columnspan=2)
        
        self.inf=tk.Label(self.frame4,text="X座標,Y座標,クリックタイプ,間隔")
        self.inf.grid(row=0,column=0,columnspan=3)
        
        self.listbox=tk.Listbox(self.frame4,width=30,height=8)
        self.listbox.grid(row=1,column=0,columnspan=3,padx=5)
        
        self.bt1=tk.Button(self.frame4,text="移動",command=self.go_pointer)
        self.bt1.grid(row=2,column=0,pady=5)
        
        self.bt2=tk.Button(self.frame4,text="変更",command=self.change)
        self.bt2.grid(row=2,column=1,pady=5)
        
        self.bt3=tk.Button(self.frame4,text="削除",command=self.list_delete)
        self.bt3.grid(row=2,column=2,pady=5)
        
        
        self.start=tk.Button(self.root,text="開始",width=8,bg="#CCE4F7", fg="black",command=self.click_start)
        self.start.grid(row=3,column=2,pady=10,padx=5)
        
        self.end=tk.Button(self.root,text="終了",width=8,command=self.root.destroy)
        self.end.grid(row=3,column=3,pady=10,padx=5)
        
        
        self.quest=tk.Button(self.root,text="メインクエスト 塔 : 連打",command=lambda:self.mememori_click(1))
        self.quest.grid(row=3,column=0)
        
        self.kenma=tk.Button(self.root,text="研磨 : 連打",command=lambda:self.mememori_click(2))
        self.kenma.grid(row=3,column=1)
        
        self.icon = tk.PhotoImage(file=resource_path("autoclicker_icon_resize.png"))
        self.root.iconphoto(True, self.icon)
        

        
    def mememori_click(self,mememori_type):
        self.quest_count=self.listbox.size()
        for i in range(self.quest_count):
            self.listbox.delete(0)
        if mememori_type==1:
            self.listbox.insert(tk.END,"1615 , 980 , 左 , 150")
        elif mememori_type==2:
            self.listbox.insert(tk.END,"950 , 950 , 左 , 100")
    
    def front(self):
        state = self.front_window.get()
        self.root.attributes('-topmost',state)
        self.menu1.entryconfig(1, label="最前面表示:ON" if state else "最前面表示:OFF")
        
        
    def click_start(self):
        if self.running:                  # 二重に押されたら無視
            return
        rows = self.listbox.get(0, tk.END)
        if not rows:                      # 一覧が空なら何もしない
            return
        A = int(self.input_start_time.get())
        C = int(self.input_click_number.get())

        self.rows = rows                  # click_step で使うので self. に保存
        self.C = C
        self.count = 0
        self.index = 0                    # いま何行目か
        self.running = True
        self.now_inf2['text'] = "実行中"
        self.root.after(A*1000, self.click_step)    # 開始時間(秒)をミリ秒にして予約

    def click_step(self):
        if not self.running:
            self.now_inf2['text'] = "停止中"
            self.clickcount2["text"]="0"
            return

        row = self.rows[self.index].split(" , ")
        row[0]=int(row[0])
        row[1]=int(row[1])
        if row[2]=="左":
            row[2]="left"
        else:
            row[2]="right"
        self.auto_clicking = True
        pyauto.click(row[0], row[1], button=row[2])
        self.auto_clicking = False
        self.count += 1
        self.clickcount2['text'] = self.count

        if self.C != 0 and self.count >= self.C:
            self.running = False
            self.now_inf2['text'] = "停止中"
            return

        self.index = (self.index + 1) % len(self.rows)
        row[3]=int(row[3])
        self.root.after(row[3], self.click_step)

    def on_press(self, key):
        if key == keyboard.Key.f12 and not self.running:
            self.root.after(0, self.mouse_pointer)
        
    def on_click(self, x, y, button, pressed, *args):
        if self.auto_clicking:
            return
        if pressed and button == mouse.Button.right and self.running:
            self.running = False

    def go_pointer(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        text=self.listbox.get(sel[0])
        text=text.split(" , ")
        text[0]=int(text[0])
        text[1]=int(text[1])
        pyauto.moveTo(text[0],text[1])
        
    def mouse_pointer(self, event=None):
        pos = pyauto.position()
        self.list_insert(pos.x, pos.y)
    
        
    def list_insert(self,X,Y):
        click_interval=self.input_time.get()
        click_type_number=self.click_type.get()
        if click_type_number==1:
            ct="左"
        elif click_type_number==2:
            ct="右"
        self.listbox.insert(tk.END, f"{X} , {Y} , {ct} , {click_interval}")
    
    def list_delete(self):
        delete_number=self.listbox.curselection()
        if delete_number:
            self.listbox.delete(delete_number[0])

    def change(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.henkou = tk.Toplevel(self.root)
        self.henkou.transient(self.root)   # root の「子」にする(タスバーに別枠で出ない)
        self.henkou.grab_set()             # 閉じるまで、root を操作できなくする
        self.henkou.title("変更")
        self.henkou.geometry("300x50")
        self.change_entry=tk.Entry(self.henkou,width=50)
        self.change_entry.grid(row=0,column=0,columnspan=4)
        
        if sel:
            text=self.listbox.get(sel[0])
        self.change_entry.insert(0,text)
        
        self.henkou_button1=tk.Button(self.henkou,text="OK",width=10,command=lambda: self.henkou_OK(sel[0]))
        self.henkou_button1.grid(row=1,column=2)
        
        self.henkou_button2=tk.Button(self.henkou,text="キャンセル",width=10,command=self.henkou.destroy)
        self.henkou_button2.grid(row=1,column=3)
    
    def henkou_OK(self,sel):
        changed_entry=self.change_entry.get()
        self.listbox.delete(sel) 
        self.listbox.insert(sel,changed_entry)
        self.henkou.destroy()


app=autoclick(root)



root.mainloop()
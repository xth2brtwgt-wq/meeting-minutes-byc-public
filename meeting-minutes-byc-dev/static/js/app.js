// Meeting Minutes BYC - JavaScript

class MeetingMinutesApp {
    constructor() {
        this.currentFile = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.showUploadCard();
        this.setupDragAndDrop();
        this.setDefaultValues();
    }
    
    setDefaultValues() {
        // 会議日時に現在の日時を設定
        document.getElementById('meetingDate').value = this.getCurrentDateTime();
    }

    setupEventListeners() {
        // ファイル選択
        document.getElementById('audioFile').addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
        });

        // ファイル処理
        document.getElementById('processFile').addEventListener('click', () => {
            this.processFile();
        });
    }

    setupDragAndDrop() {
        const uploadArea = document.getElementById('uploadArea');
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });

        uploadArea.addEventListener('click', () => {
            document.getElementById('audioFile').click();
        });
    }


    showUploadCard() {
        document.getElementById('uploadCard').style.display = 'block';
    }

    updateStatus(type, title, message) {
        const statusCard = document.getElementById('statusCard');
        const icon = statusCard.querySelector('.status-icon');
        const titleElement = statusCard.querySelector('h3');
        const messageElement = statusCard.querySelector('p');

        // アイコンの更新
        const icons = {
            'ready': '✅',
            'warning': '⚠️',
            'error': '❌',
            'processing': '⏳'
        };
        icon.textContent = icons[type] || '🔧';

        // タイトルとメッセージの更新
        titleElement.textContent = title;
        messageElement.textContent = message;

        // ステータスカードの表示
        statusCard.style.display = 'flex';
    }

    handleFileSelect(file) {
        if (!file) return;

        // ファイル形式のチェック
        const allowedTypes = ['audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/m4a', 'audio/flac', 'audio/ogg', 'audio/webm'];
        if (!allowedTypes.includes(file.type)) {
            alert('サポートされていないファイル形式です。\n対応形式: WAV, MP3, M4A, FLAC, OGG, WEBM');
            return;
        }

        // ファイルサイズのチェック（100MB制限）
        const maxSize = 100 * 1024 * 1024; // 100MB
        if (file.size > maxSize) {
            alert('ファイルサイズが大きすぎます。\n最大100MBまで対応しています。');
            return;
        }

        this.currentFile = file;
        this.displayFileInfo(file);
    }

    displayFileInfo(file) {
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');

        fileName.textContent = `ファイル名: ${file.name}`;
        fileSize.textContent = `サイズ: ${this.formatFileSize(file.size)}`;

        fileInfo.style.display = 'block';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async processFile() {
        if (!this.currentFile) {
            alert('ファイルが選択されていません。');
            return;
        }

        // ボタン押下時に即座にメッセージを表示
        this.showProcessingMessage();

        try {
            const formData = new FormData();
            formData.append('audio', this.currentFile);
            
                // 追加パラメータの取得
                const meetingDate = document.getElementById('meetingDate').value;
                const conditions = document.getElementById('conditions').value;
                const email = document.getElementById('email').value;
                
                if (meetingDate) formData.append('meeting_date', meetingDate);
                if (conditions) formData.append('conditions', conditions);
                if (email) formData.append('email', email);
                // Notion登録は常に実行
                formData.append('send_to_notion', 'true');

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'サーバーエラーが発生しました');
            }

            const result = await response.json();
            this.showResult(result);

        } catch (error) {
            console.error('Error:', error);
            alert('エラーが発生しました: ' + error.message);
            this.hideProcessingMessage();
            this.enableButtons(); // エラー時もボタンを有効化
        }
    }



    showProcessingMessage() {
        // アップロードカードを非表示
        document.getElementById('uploadCard').style.display = 'none';
        
        // 処理中メッセージを表示
        document.getElementById('resultCard').style.display = 'block';
        document.getElementById('resultSummary').innerHTML = `
            <h3>⏳ 処理中...</h3>
            <div class="completion-message">
                <p>🎤 音声ファイルを処理中です...</p>
                <p>📧 処理完了後、メールが送信されます。後でメールをご確認ください。</p>
                <p>⏱️ 処理には数分かかる場合があります。</p>
            </div>
        `;
        
        // タブを非表示（削除済みの要素のためコメントアウト）
        // document.querySelector('.result-tabs').style.display = 'none';
        // document.querySelector('.result-content').style.display = 'none';
        
        // ボタンを無効化
        this.disableButtons();
    }

    hideProcessingMessage() {
        // アップロードカードを再表示
        document.getElementById('uploadCard').style.display = 'block';
        document.getElementById('resultCard').style.display = 'none';
        
        // ボタンを有効化
        this.enableButtons();
    }

    disableButtons() {
        // 処理ボタンを無効化
        const processBtn = document.getElementById('processFile');
        if (processBtn) {
            processBtn.disabled = true;
            processBtn.textContent = '処理中...';
        }
        
        // 削除されたボタンのためコメントアウト
        // const newFileBtn = document.getElementById('newFileBtn');
        // if (newFileBtn) {
        //     newFileBtn.disabled = true;
        // }
        
        // const downloadBtn = document.getElementById('downloadBtn');
        // if (downloadBtn) {
        //     downloadBtn.disabled = true;
        // }
    }

    enableButtons() {
        // 処理ボタンを有効化
        const processBtn = document.getElementById('processFile');
        if (processBtn) {
            processBtn.disabled = false;
            processBtn.textContent = '文字起こし・議事録生成';
        }
        
        // 削除されたボタンのためコメントアウト
        // const newFileBtn = document.getElementById('newFileBtn');
        // if (newFileBtn) {
        //     newFileBtn.disabled = false;
        // }
        
        // const downloadBtn = document.getElementById('downloadBtn');
        // if (downloadBtn) {
        //     downloadBtn.disabled = false;
        // }
    }

    showResult(result) {
        // 結果カードの表示
        document.getElementById('resultCard').style.display = 'block';
        
        // メール送信ステータスの表示
        this.updateEmailStatus(result);
        
        // Notion登録ステータスの表示
        this.updateNotionStatus(result);
        
        // 結果をローカルストレージに保存
        localStorage.setItem('lastResult', JSON.stringify(result));
        
        // ボタンを有効化
        this.enableButtons();
    }

    updateEmailStatus(result) {
        const emailStatusValue = document.getElementById('emailStatusValue');
        if (!emailStatusValue) return;

        const emailSent = result.email_sent;
        const emailAddress = result.email_address;
        const emailError = result.email_error;

        if (emailSent === true) {
            emailStatusValue.innerHTML = `<span style="color: green;">✅ 送信完了 (${emailAddress})</span>`;
        } else if (emailSent === false && emailError) {
            emailStatusValue.innerHTML = `<span style="color: red;">❌ 送信失敗: ${emailError}</span>`;
        } else if (emailSent === false && !emailAddress) {
            emailStatusValue.innerHTML = `<span style="color: orange;">⚠️ メール送信: 未設定</span>`;
        } else {
            emailStatusValue.innerHTML = `<span style="color: gray;">❓ 不明</span>`;
        }
    }

    updateNotionStatus(result) {
        const notionStatusValue = document.getElementById('notionStatusValue');
        if (!notionStatusValue) return;

        const notionSent = result.notion_sent;
        const notionPageId = result.notion_page_id;
        const notionError = result.notion_error;

        if (notionSent === true && notionPageId) {
            notionStatusValue.innerHTML = `<span style="color: green;">✅ 登録完了</span>`;
        } else if (notionSent === false && notionError) {
            notionStatusValue.innerHTML = `<span style="color: red;">❌ 登録失敗: ${notionError}</span>`;
        } else if (notionSent === false) {
            notionStatusValue.innerHTML = `<span style="color: orange;">⚠️ 登録: 未実行</span>`;
        } else {
            notionStatusValue.innerHTML = `<span style="color: gray;">❓ 不明</span>`;
        }
    }

    backToTop() {
        // トップ画面に戻る
        this.resetForm();
    }

    resetForm() {
        // フォームのリセット
        document.getElementById('audioFile').value = '';
        document.getElementById('meetingDate').value = this.getCurrentDateTime(); // 現在の日時を設定
        document.getElementById('conditions').value = '';
        document.getElementById('email').value = 'mipatago.netsetting@gmail.com'; // デフォルト値を保持
        document.getElementById('fileInfo').style.display = 'none';
        document.getElementById('resultCard').style.display = 'none';
        
        // ファイル情報のクリア
        this.currentFile = null;
        
        // アップロードカードの表示
        document.getElementById('uploadCard').style.display = 'block';
    }
    
    getCurrentDateTime() {
        // 現在の日時をdatetime-local形式で取得
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        return `${year}-${month}-${day}T${hours}:${minutes}`;
    }
}

// トップ画面に戻る機能
function backToTop() {
    const app = new MeetingMinutesApp();
    app.backToTop();
}

// アプリケーションの初期化
document.addEventListener('DOMContentLoaded', () => {
    new MeetingMinutesApp();
});

from flask import Flask, render_template, request, redirect, url_for, flash
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv



load_dotenv()


app = Flask(__name__)
app.secret_key = '1212121212132435rgtnbternt6rnm6t5j6yu64'  # Necessário para usar mensagens flash

# Configurações do Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SPREADSHEET_ID = '1rnfMQBHy6prX--t89hgSt14hh9J7mwBRhN5B8tMDY68'
RANGE_NAME = 'Produtividade!A:D'
# Credenciais da conta de serviço
creds = Credentials.from_service_account_file('client_secret.json', scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def get_records():
    try:
        # Ler dados da planilha
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        records = result.get('values', [])
        return records
    except Exception as e:
        flash(f'Erro ao ler a planilha: {str(e)}', 'error')
        return []

def get_next_id(records):
    # Encontra o maior ID e retorna o próximo ID
    ids = [int(record[0]) for record in records if record[0].isdigit()]
    return max(ids) + 1 if ids else 1  # Retorna 1 se não houver IDs existentes

def update_sheet(records):
    try:
        # Atualizar a planilha com novos dados
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                              valueInputOption="RAW", body={"values": records}).execute()
        flash('Planilha atualizada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar a planilha: {str(e)}', 'error')

@app.route('/')
def index():
    # Obter todos os registros
    records = get_records()
    
    # Calcular o próximo ID com base no número de registros + 1
    next_id = len(records) + 1
    
    return render_template('index.html', records=records, next_id=next_id)

@app.route('/update', methods=['POST'])
def update():
    try:
        # Manipular os dados do formulário enviado para edição, exclusão ou adição
        records = get_records()
        new_records = []
        for record in records:
            if record[0] != request.form['ID']:  # Excluir ou editar registro com base no ID
                new_records.append(record)
            if record[0] == request.form['ID']:  # Editar o registro existente
                record[1] = request.form['NOME']
                record[2] = request.form['EMPRESA']
                record[3] = request.form['OBRA']
                new_records.append(record)

        if 'new_record' in request.form:  # Adicionar novo registro
            new_records.append([request.form['ID'], request.form['NOME'], request.form['EMPRESA'], request.form['OBRA']])

        update_sheet(new_records)
    except Exception as e:
        flash(f'Erro ao atualizar a planilha: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/adiciona_funcionario', methods=['POST'])
def adiciona_funcionario():
    try:
        # Obter os registros atuais da planilha
        records = get_records()
        new_records = []

        record_id = request.form.get('ID')
        is_new_record = 'new_record' in request.form

        # Se é um novo registro, encontrar o próximo ID auto-incrementável
        if is_new_record:
            max_id = max(int(record[0]) for record in records if record[0].isdigit()) if records else 0
            record_id = str(max_id + 1)

        record_found = False
        for record in records:
            if record[0] == record_id:  # Se o ID coincidir, editar o registro
                record[1] = request.form['NOME']
                record[2] = request.form['EMPRESA']
                record[3] = request.form['OBRA']
                record_found = True
            else:  # Manter os registros que não estão sendo editados
                new_records.append(record)

        # Se for um novo registro e não foi encontrado anteriormente
        if not record_found and is_new_record:
            new_records.append([
                record_id,
                request.form['NOME'],
                request.form['EMPRESA'],
                request.form['OBRA']
            ])

        # Atualizar a planilha com os novos registros
        update_sheet(new_records)

    except Exception as e:
        flash(f'Erro ao atualizar a planilha: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    try:
        # Obter os registros atuais da planilha
        records = get_records()
        print(f"Registros antes da exclusão: {records}")

        # Filtrar registros para remover o registro com o ID especificado
        new_records = [record for record in records if record[0] != id]
        print(f"Registros após exclusão: {new_records}")

        # Limpar a planilha
        clear_sheet()

        # Atualizar a planilha com os registros filtrados
        update_sheet(new_records)
        
    except Exception as e:
        flash(f'Erro ao excluir o registro: {str(e)}', 'error')

    return redirect(url_for('index'))



def clear_sheet():
    try:
        # Limpa todos os dados na planilha
        sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    except Exception as e:
        flash(f'Erro ao limpar a planilha: {str(e)}', 'error')


def delete_row_by_id(employee_id, range_name, sheet_id):
    service = authenticate()
    spreadsheet_id = '1rnfMQBHy6prX--t89hgSt14hh9J7mwBRhN5B8tMDY68'
    values = get_values(range_name)
    
    row_index = None
    for i, row in enumerate(values):
        if str(row[0]) == str(employee_id):
            row_index = i + 1  # 1-based index for API
            break
    
    if row_index is not None:
        request_body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": sheet_id,
                            "dimension": "ROWS",
                            "startIndex": row_index - 1,  # 0-based index for API
                            "endIndex": row_index
                        }
                    }
                }
            ]
        }
        
        try:
            response = service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            ).execute()
            return response
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    return None



@app.route('/search', methods=['GET'])
def search():
    id_query = request.args.get('id', '')
    name_query = request.args.get('name', '')
    company_query = request.args.get('company', '')
    location_query = request.args.get('location', '')

    try:
        records = get_records()
        filtered_records = [
            record for record in records
            if (id_query.lower() in record[0].lower() if id_query else True) and
               (name_query.lower() in record[1].lower() if name_query else True) and
               (company_query.lower() in record[2].lower() if company_query else True) and
               (location_query.lower() in record[3].lower() if location_query else True)
        ]
        return {'records': filtered_records}
    except Exception as e:
        flash(f'Erro ao buscar registros: {str(e)}', 'error')
        return {'records': []}
    

#if __name__ == "__main__":
   # app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    #ISTO RODA EM TODAS PLATAFORMAS

if __name__ == '__main__':
    app.run(debug=True)
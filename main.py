import os
from pathlib import Path
from dash_extensions.enrich import Dash, Input, Output, State, Trigger, callback, ALL, MATCH
from dash import dcc, _dash_renderer
from dash.html import Div, Label
import dash_mantine_components as dmc
from dash_local_react_components import load_react_component
import ai
from magi.brains.melchior import MELCHIOR_PERSONALITY
from magi.brains.balthasar import BALTHASAR_PERSONALITY
from magi.brains.casper import CASPER_PERSONALITY


def _load_local_env(path: str = ".env") -> None:
    """
    Lightweight .env loader for local development.
    """
    candidate_paths = [
        Path(path),  # current working directory
        Path(__file__).resolve().parent / path,  # project root
    ]

    for env_path in candidate_paths:
        if not env_path.exists():
            continue

        for raw_line in env_path.read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                # .env is authoritative for local runs.
                os.environ[key] = value


_load_local_env()

# Fast defaults for responsive UI; override in .env if needed.
os.environ.setdefault("MAGI_FAST_MODE", "1")
os.environ.setdefault("MAGI_MAX_DELIBERATION_ROUNDS", "1")
os.environ.setdefault("MAGI_ENABLE_CROSS_EXAMINATION", "0")
os.environ.setdefault("MAGI_MODEL", "gpt-5")

# Mantine components require React 18 hooks (e.g., useSyncExternalStore).
_dash_renderer._set_react_version("18.2.0", "18.2.0")

app = Dash(__name__)

Magi = load_react_component(app, 'components', 'magi.js')
WiseMan = load_react_component(app, 'components', 'wise_man.js')
Response = load_react_component(app, 'components', 'response.js')
Modal = load_react_component(app, 'components', 'modal.js')
Header = load_react_component(app, 'components', 'header.js')
Status = load_react_component(app, 'components', 'status.js')

app.layout = dmc.MantineProvider(
    children=[
        Div(
            className='system',
            children=[
                Magi(id='magi', children=[
                    Header(side='left', title='質 問'),
                    Header(side='right', title='解 決'),
                    Status(id='status'),
                    WiseMan(
                        id={'type': 'wise-man', 'name': 'melchior'},
                        name='melchior',
                        order_number=1,
                        personality=MELCHIOR_PERSONALITY.build_system_prompt()),
                    WiseMan(
                        id={'type': 'wise-man', 'name': 'balthasar'},
                        name='balthasar',
                        order_number=2,
                        personality=BALTHASAR_PERSONALITY.build_system_prompt()),
                    WiseMan(
                        id={'type': 'wise-man', 'name': 'casper'},
                        name='casper',
                        order_number=3,
                        personality=CASPER_PERSONALITY.build_system_prompt()),
                    Response(id='response', status='info')
                ]),
                Div(className='input-container', children=[
                    Label('access code: '),
                    dcc.Input(
                        id='key',
                        autoComplete='off',
                        type='password',
                        value='',
                        placeholder='Using OPENAI_API_KEY from .env',
                        disabled=True
                    ),
                    Label('question: '),
                    dcc.Input(id='query', type='text', value='', debounce=True, autoComplete='off'),
                ]),
                Modal(id={'type': 'modal', 'name': 'melchior'}, name='melchior'),
                Modal(id={'type': 'modal', 'name': 'balthasar'}, name='balthasar'),
                Modal(id={'type': 'modal', 'name': 'casper'}, name='casper'),

                dcc.Store(id='question', data={'id': 0, 'query': ''}),
                dcc.Store(id='annotated-question', data={'id': 0, 'query': '', 'is_yes_or_no_question': False}),
                dcc.Store(id='is_yes_or_no_question', data=False),
                dcc.Store(id='question-id', data=0),
            ]
        )
    ]
)


@callback(
    Output('question', 'data'),
    Input('query', 'value'),
    State('question', 'data'),
    prevent_initial_call=True)
def question(query: str, question: dict):
    return {'id': question['id'] + 1, 'query': query}


@callback(
    Output('annotated-question', 'data'),
    Input('question', 'data'),
    prevent_initial_call=True)
def annotated_question(question: dict):
    try:
        is_yes_or_no_question = ai.is_yes_or_no_question(question['query'], '')

        return {
            'id': question['id'],
            'query': question['query'],
            'is_yes_or_no_question': is_yes_or_no_question,
            'error': None
        }
    except Exception as e:
        return {
            'id': question['id'],
            'query': question['query'],
            'is_yes_or_no_question': False,
            'error': str(e)
        }


@callback(
    Output('status', 'extention'),
    Input('question', 'data'),
    Input('annotated-question', 'data'))
def extention(question: dict, annotated_question: dict):
    if question['id'] != annotated_question['id']:
        return '????'

    return '7312' if annotated_question['is_yes_or_no_question'] else '3023'


@callback(
    Output({'type': 'wise-man', 'name': MATCH}, 'answer'),
    Input('annotated-question', 'data'),
    State({'type': 'wise-man', 'name': MATCH}, 'personality'),
    prevent_initial_call=True)
def wise_man_answer(question: dict, personality: str):
    if question['error']:
        return {'id': question['id'], 'response': question['error'], 'status': 'error'}

    try:
        answer = ai.get_answer(question['query'], personality, '')

        if question['is_yes_or_no_question']:
            classification = ai.classify_answer(question['query'], personality, answer, '')
        else:
            classification = {'status': 'info', 'conditions': None}

        return {'id': question['id'], 'response': answer, 'status': classification['status'], 'conditions': classification['conditions'], 'error': None}

    except Exception as e:
        return {'id': question['id'], 'response': None, 'status': 'error', 'conditions': 'None', 'error': str(e)}


@callback(
    Output({'type': 'wise-man', 'name': MATCH}, 'question_id'),
    Input('question', 'data'))
def wise_man_question_id(question: dict):
    return question['id']


@callback(
    Output('response', 'question_id'),
    Input('question', 'data'))
def response_question_id(question: dict):
    return question['id']


@callback(
    Output('response', 'status'),
    Output('response', 'answer_id'),
    Input({'type': 'wise-man', 'name': ALL}, 'answer'),
    prevent_initial_call=True)
def response_status(answers: list):
    answer_id = min([answer['id'] for answer in answers])
    status = 'info'

    if any([answer['status'] == 'error' for answer in answers]):
        status = 'error'
    elif any([answer['status'] == 'no' for answer in answers]):
        status = 'no'
    elif any([answer['status'] == 'conditional' for answer in answers]):
        status = 'conditional'
    elif all([answer['status'] == 'yes' for answer in answers]):
        status = 'yes'

    return status, answer_id


@callback(
    Output({'type': 'modal', 'name': MATCH}, 'is_open'),
    Trigger({'type': 'wise-man', 'name': MATCH}, 'n_clicks'),
    prevent_initial_call=True)
def modal_visibility():
    return True


@callback(
    Output({'type': 'modal', 'name': MATCH}, 'question'),
    Output({'type': 'modal', 'name': MATCH}, 'answer'),
    Input('question', 'data'),
    Input({'type': 'wise-man', 'name': MATCH}, 'answer'))
def modal_content(question: dict, answer: dict):
    return question, answer


if __name__ == '__main__':
    app.run_server(debug=True)

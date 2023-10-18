# load secrets
import dotenv
dotenv.load_dotenv('/home/oscar/nlitp/eva_proof_server/.env')

import evadb
cursor = evadb.connect(evadb_dir='/home/oscar/nlitp/eva_proof_server/evadb_data').cursor()
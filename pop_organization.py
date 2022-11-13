import sys, psycopg2, ldap
from ldap import modlist

def pop(**kargs):

    print(user,senha)
    con = psycopg2.connect("host=post dbname=authdb user=%s password=%s"%(user,senha))
    cur = con.cursor()

    cur.execute("INSERT INTO secao (nm_sigla, in_excluido) VALUES (%s,%s) RETURNING id_secao;", ("Chefia","n"))
    id_secao_pai = cur.fetchone()[0]
    cur.execute("INSERT INTO secao (id_pai, nm_sigla, in_excluido) VALUES (%s,%s,%s);", (id_secao_pai,"RH","n"))
    cur.execute("INSERT INTO secao (id_pai, nm_sigla, in_excluido) VALUES (%s,%s,%s);", (id_secao_pai,"Operações","n"))
    cur.execute("INSERT INTO secao (id_pai, nm_sigla, in_excluido) VALUES (%s,%s,%s);", (id_secao_pai,"Informática","n"))
    cur.execute("INSERT INTO secao (id_pai, nm_sigla, in_excluido) VALUES (%s,%s,%s);", (id_secao_pai,"Aprovisionamento","n"))
    cur.execute("INSERT INTO secao (id_pai, nm_sigla, in_excluido) VALUES (%s,%s,%s);", (id_secao_pai,"Serviços Gerais","n"))
    cur.execute("INSERT INTO secao (id_pai, nm_sigla, in_excluido) VALUES (%s,%s,%s);", (id_secao_pai,"Manutenção e Transporte","n"))

    cur.execute("INSERT INTO secao (id_pai, nm_sigla, in_excluido) VALUES (%s,%s,%s) RETURNING id_secao;", (id_secao_pai,"Almoxarifado","n"))
    id_secao_almox = cur.fetchone()[0]
    cur.execute("INSERT INTO usuario (nm_usuario, in_excluido) VALUES (%s,%s) RETURNING id_usuario;", ("Ch Almox", "n"))
    id_usuario_chalmox = cur.fetchone()[0]
    cur.execute("INSERT INTO secao (id_pai, nm_sigla, in_excluido) VALUES (%s,%s,%s) RETURNING id_secao;", (id_secao_pai,"Aquisições","n"))
    id_secao_aquisicoes = cur.fetchone()[0]
    cur.execute("INSERT INTO usuario (nm_usuario, in_excluido) VALUES (%s,%s) RETURNING id_usuario;", ("Ch SALC", "n"))
    id_usuario_chsalc = cur.fetchone()[0]
    cur.execute("INSERT INTO pessoa (nm_login, nm_completo, cd_patente, nm_guerra) VALUES (%s,%s,%s,%s) RETURNING id_pessoa", ("capfoo", "Foo Bar", "8", "Foo"))
    id_pessoa = cur.fetchone()[0]
    cur.execute("INSERT INTO usuario_pessoa (id_usuario, id_pessoa) VALUES (%s,%s)", (id_usuario_chalmox, id_pessoa))
    cur.execute("INSERT INTO usuario_secao (id_usuario, id_secao) VALUES (%s,%s)", (id_usuario_chsalc, id_secao_aquisicoes))
    cur.execute("INSERT INTO usuario_secao (id_usuario, id_secao) VALUES (%s,%s)", (id_usuario_chalmox, id_secao_almox))
    con.commit()

    print(id_secao_aquisicoes,id_pessoa,id_usuario_chsalc)
    
    con2 = psycopg2.connect("host=post dbname=requisicoes user=%s password=%s"%(user,senha))
    cur2 = con2.cursor()
    cur2.execute("INSERT INTO configuracao (contas_salc,conta_fiscal,conta_od) VALUES (%s,%s,%s)", ([id_usuario_chalmox],id_usuario_chalmox,id_usuario_chalmox))
    con2.commit()
    # Close communication with the database
    cur.close()
    con.close()
    cur2.close()
    con2.close()

    try:
        l = ldap.initialize('ldap://ldap')
        username = "cn=admin,dc=eb,dc=mil,dc=br"
        password = 'secret'
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(username, password)
        attrs = {}
        attrs['objectClass'] = [b"person", b"organizationalPerson", b"inetOrgPerson", b"posixAccount"]
        attrs['uid'] = [b'capfoo']
        attrs['cn'] = [b'capfoo']
        attrs['givenname'] = [b'Foo']
        attrs['sn'] = [b'Bar']
        attrs['mail'] = [b'email']
        attrs['uidNumber'] = [b'1000']
        attrs['gidNumber'] = [b'5000']
        attrs['loginShell'] = [b'bash']
        attrs['homeDirectory'] = [b'/']
        attrs['userPassword'] = [b'12345']
        ldif = modlist.addModlist(attrs)
        l.add_s("cn=capfoo,dc=eb,dc=mil,dc=br",ldif)
        l.unbind_s()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    user = "postgres"
    senha = "secret"
    if len(sys.argv)==2:
        senha = sys.argv[1]
    elif len(sys.argv)>2:
        user = sys.argv[1]
        senha = sys.argv[2]
    pop(user=user, senha=senha)
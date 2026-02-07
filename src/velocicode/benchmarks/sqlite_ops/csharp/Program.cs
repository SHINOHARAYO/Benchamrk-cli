using System;
using System.IO;
using Microsoft.Data.Sqlite;

class Program
{
    static void Main(string[] args)
    {
        int n = 10000;
        if (args.Length > 0)
        {
            int.TryParse(args[0], out n);
        }

        string dbPath = "bench.db";
        if (File.Exists(dbPath))
        {
            File.Delete(dbPath);
        }

        using (var connection = new SqliteConnection($"Data Source={dbPath}"))
        {
            connection.Open();

            var command = connection.CreateCommand();
            command.CommandText = "CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)";
            command.ExecuteNonQuery();

            using (var transaction = connection.BeginTransaction())
            {
                var insertCmd = connection.CreateCommand();
                insertCmd.CommandText = "INSERT INTO test (value) VALUES ($value)";
                var parameter = insertCmd.CreateParameter();
                parameter.ParameterName = "$value";
                insertCmd.Parameters.Add(parameter);
                insertCmd.Transaction = transaction;

                for (int i = 0; i < n; i++)
                {
                    parameter.Value = $"value-{i}";
                    insertCmd.ExecuteNonQuery();
                }

                transaction.Commit();
            }

            var selectCmd = connection.CreateCommand();
            selectCmd.CommandText = "SELECT * FROM test";
            using (var reader = selectCmd.ExecuteReader())
            {
                int count = 0;
                while (reader.Read())
                {
                    count++;
                }
            }
        }

        if (File.Exists(dbPath))
        {
            File.Delete(dbPath);
        }
    }
}

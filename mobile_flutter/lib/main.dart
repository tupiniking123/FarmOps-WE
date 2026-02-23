import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const FarmSaaSApp());
}

class FarmSaaSApp extends StatelessWidget {
  const FarmSaaSApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FarmSaaS Rural',
      theme: ThemeData(colorSchemeSeed: Colors.green, useMaterial3: true),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  String _health = 'checking...';
  final TextEditingController _tenantName = TextEditingController();
  final TextEditingController _tenantEmail = TextEditingController();
  final List<Map<String, dynamic>> _tenants = [];

  static const String apiBaseUrl = 'http://localhost:8000';

  @override
  void initState() {
    super.initState();
    _loadHealth();
    _loadTenants();
  }

  Future<void> _loadHealth() async {
    try {
      final res = await http.get(Uri.parse('$apiBaseUrl/health'));
      setState(() => _health = res.statusCode == 200 ? 'online' : 'error');
    } catch (_) {
      setState(() => _health = 'offline');
    }
  }

  Future<void> _loadTenants() async {
    final res = await http.get(Uri.parse('$apiBaseUrl/tenants'));
    if (res.statusCode == 200) {
      final data = List<Map<String, dynamic>>.from(jsonDecode(res.body));
      setState(() {
        _tenants
          ..clear()
          ..addAll(data);
      });
    }
  }

  Future<void> _createTenant() async {
    final payload = jsonEncode({'name': _tenantName.text, 'email': _tenantEmail.text});
    final res = await http.post(
      Uri.parse('$apiBaseUrl/tenants'),
      headers: {'Content-Type': 'application/json'},
      body: payload,
    );
    if (res.statusCode == 200) {
      _tenantName.clear();
      _tenantEmail.clear();
      await _loadTenants();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('FarmSaaS Rural (Windows + Android)')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('API status: $_health'),
            const SizedBox(height: 16),
            TextField(controller: _tenantName, decoration: const InputDecoration(labelText: 'Nome da empresa')),
            TextField(controller: _tenantEmail, decoration: const InputDecoration(labelText: 'E-mail')),
            const SizedBox(height: 8),
            FilledButton(onPressed: _createTenant, child: const Text('Criar tenant')),
            const Divider(height: 24),
            const Text('Tenants cadastrados:'),
            Expanded(
              child: ListView.builder(
                itemCount: _tenants.length,
                itemBuilder: (context, i) => ListTile(
                  title: Text(_tenants[i]['name']?.toString() ?? ''),
                  subtitle: Text(_tenants[i]['email']?.toString() ?? ''),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
